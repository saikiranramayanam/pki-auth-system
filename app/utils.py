import base64
import pyotp
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

PRIVATE_KEY_PATH = "/app/student_private.pem"

# -------------------------
# TOTP GENERATOR
# -------------------------
def compute_totp(seed_bytes: bytes, timestamp: int = None) -> str:
    """
    Compute a 6-digit TOTP from raw seed bytes.
    Uses SHA1, 30s interval (pyotp default).
    """
    if not isinstance(seed_bytes, (bytes, bytearray)):
        raise ValueError("seed must be raw bytes")

    # Convert bytes → Base32
    b32 = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(b32, digits=6, interval=30)

    if timestamp is None:
        return totp.now()

    return totp.at(timestamp)


# -------------------------
# RSA DECRYPT SEED
# -------------------------
def decrypt_seed(enc: str) -> bytes:
    try:
        encrypted_bytes = base64.b64decode(enc)

        with open(PRIVATE_KEY_PATH, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )

        decrypted = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted

    except Exception as e:
        raise ValueError("Seed decryption failed") from e
