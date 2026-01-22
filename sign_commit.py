from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# ---- UPDATE YOUR HASH HERE ----
commit_hash = b"108cf0d0cc6c7e7c768dcc975c98fa45ee2bb77e"

# Load student private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Sign using RSA-PSS-SHA256
signature = private_key.sign(
    commit_hash,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    ),
    hashes.SHA256(),
)

# Save raw signature
with open("signature.bin", "wb") as f:
    f.write(signature)

print("Signature created and saved to signature.bin")
