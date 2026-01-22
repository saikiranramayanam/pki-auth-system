from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from .utils import compute_totp, decrypt_seed
import time
app = FastAPI()

SEED_PATH = "/data/seed.txt"

# -----------------------------
# Request models
# -----------------------------
class DecryptRequest(BaseModel):
    encrypted_seed: str

class CodeRequest(BaseModel):
    code: str


@app.get("/")
def home():
    return {"message": "Server is running"}


# -----------------------------
# 1) DECRYPT SEED
# -----------------------------
@app.post("/decrypt-seed")
def decrypt_seed_api(data: DecryptRequest):
    try:
        decrypted_seed = decrypt_seed(data.encrypted_seed)

        # MUST write to /data/seed.txt
        with open(SEED_PATH, "wb") as f:
            f.write(decrypted_seed)

        return {"status": "ok"}

    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")


# -----------------------------
# Helper: read seed safely
# -----------------------------
def read_seed() -> bytes:
    if not os.path.exists(SEED_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_PATH, "rb") as f:
        return f.read().strip()


# -----------------------------
# 2) GENERATE 2FA TOTP
# -----------------------------
@app.get("/generate-2fa")
def generate_2fa():
    seed = read_seed()

    # DO NOT pass time manually
    code = compute_totp(seed)

    return {
        "code": code,
        "valid_for": 30
    }


# -----------------------------
# 3) VERIFY 2FA TOTP
# -----------------------------
@app.post("/verify-2fa")
def verify_2fa(data: CodeRequest):
    seed = read_seed()
    now = int(time.time())

    # Check current, previous, and next 30s window
    for offset in (-30, 0, 30):
        if compute_totp(seed, now + offset) == data.code:
            return {"valid": True}

    return {"valid": False}