from fastapi import FastAPI
from pydantic import BaseModel
import time
import base64
from .utils import compute_totp, decrypt_seed

app = FastAPI()

# Load seed.txt (may be empty before decrypt-seed is called)
try:
    with open("seed.txt", "rb") as f:
        SEED = f.read().strip()
except FileNotFoundError:
    SEED = b""

# Request models
class VerifyRequest(BaseModel):
    roll: str
    timestamp: int

class DecryptRequest(BaseModel):
    encrypted_seed: str

class CodeRequest(BaseModel):
    code: str


@app.get("/")
def home():
    return {"message": "Server is running"}


# -----------------------------
# 1) DECRYPT SEED (writes seed.txt)
# -----------------------------
@app.post("/decrypt-seed")
def decrypt_seed_api(data: DecryptRequest):
    global SEED

    # decrypt base64 → seed hex bytes
    decrypted_seed = decrypt_seed(data.encrypted_seed)

    # Save decrypted seed to seed.txt
    with open("seed.txt", "wb") as f:
        f.write(decrypted_seed)

    # Update memory
    SEED = decrypted_seed

    return {"status": "ok"}


# -----------------------------
# 2) GENERATE 2FA TOTP
# -----------------------------
@app.get("/generate-2fa")
def generate_2fa():
    if not SEED:
        return {"error": "seed.txt is not loaded yet"}

    current_time = int(time.time())
    code = compute_totp(SEED, current_time)

    return {"code": code, "valid_for": 30}


# -----------------------------
# 3) VERIFY 2FA TOTP
# -----------------------------
@app.post("/verify-2fa")
def verify_2fa(data: CodeRequest):
    if not SEED:
        return {"error": "seed.txt is not loaded yet"}

    current_time = int(time.time())
    correct_code = compute_totp(SEED, current_time)

    return {"valid": data.code == correct_code}


# -----------------------------
# 4) ORIGINAL VERIFY ENDPOINT
# -----------------------------
@app.post("/verify")
def verify(data: VerifyRequest):
    totp_code = compute_totp(SEED, data.timestamp)

    return {
        "student_roll": data.roll,
        "timestamp": data.timestamp,
        "totp": totp_code
    }
