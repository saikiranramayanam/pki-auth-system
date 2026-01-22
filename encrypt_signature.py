import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load instructor public key
with open("instructor_public.pem", "rb") as f:
    instructor_pub = serialization.load_pem_public_key(f.read())

# Load raw signature
with open("signature.bin", "rb") as f:
    signature = f.read()

# Encrypt using RSA-OAEP-SHA256
encrypted = instructor_pub.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
)

# Base64 encode and save
with open("encrypted_signature.txt", "wb") as f:
    f.write(base64.b64encode(encrypted))

print("Encrypted signature saved to encrypted_signature.txt")
