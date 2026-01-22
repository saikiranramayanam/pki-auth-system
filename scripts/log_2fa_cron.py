#!/usr/bin/env python3

import os
import datetime
import base64
import pyotp

SEED_FILE = "/data/seed.txt"

def main():
    if not os.path.exists(SEED_FILE):
        return

    with open(SEED_FILE, "rb") as f:
        seed_bytes = f.read().strip()

    b32 = base64.b32encode(seed_bytes).decode()
    totp = pyotp.TOTP(b32, digits=6, interval=30)

    code = totp.now()
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{timestamp} - 2FA Code: {code}")

if __name__ == "__main__":
    main()
