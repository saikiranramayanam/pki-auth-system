import base64
import binascii
import pyotp
import hmac
import hashlib
import time


# -------------------------
# FIXED TOTP GENERATOR
# -------------------------

def compute_totp(seed_bytes: bytes, timestamp: int = None) -> str:
    """
    Compute a 6-digit TOTP from seed bytes.
    timestamp = Unix time (default = now)
    """
    if not isinstance(seed_bytes, (bytes, bytearray)):
        raise ValueError("seed must be raw bytes")

    # convert bytes -> Base32
    b32 = base64.b32encode(seed_bytes).decode()

    # TOTP object
    totp = pyotp.TOTP(b32, digits=6, interval=30)

    # default timestamp = current time
    if timestamp is None:
        return totp.now()

    # generate TOTP for a specific timestamp
    return totp.at(timestamp)


# -------------------------
# DECRYPT SEED FUNCTION (BASE64 DECODE)
# -------------------------

def decrypt_seed(enc: str) -> bytes:
    try:
        return base64.b64decode(enc)
    except Exception:
        raise ValueError("Invalid encrypted_seed value")
