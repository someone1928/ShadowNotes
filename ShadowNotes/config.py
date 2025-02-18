import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

PASSWORD_SALT_FILE = "data/salt.salt"
PASSWORD_HASH_FILE = "data/password.hash"
FAILED_ATTEMPTS_FILE = "data/failed_attempts.txt"


def get_salt():
    if os.path.exists(PASSWORD_SALT_FILE):
        with open(PASSWORD_SALT_FILE, "rb") as file:
            return file.read()
    else:
        salt = os.urandom(16)
        os.makedirs("data", exist_ok=True)
        with open(PASSWORD_SALT_FILE, "wb") as file:
            file.write(salt)
        return salt

def derive_key(password: str):
    salt = get_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def get_cipher(password: str):
    key = derive_key(password)
    return Fernet(key)

def save_password_hash(password):
    key = derive_key(password)
    with open(PASSWORD_HASH_FILE, "wb") as file:
        file.write(key)

def verify_password(password):
    if not os.path.exists(PASSWORD_HASH_FILE):
        save_password_hash(password)
        return True
    with open(PASSWORD_HASH_FILE, "rb") as file:
        stored_key = file.read()
    return stored_key == derive_key(password)

def get_failed_attempts():
    if os.path.exists(FAILED_ATTEMPTS_FILE):
        with open(FAILED_ATTEMPTS_FILE, "r") as file:
            return int(file.read().strip())
    return 0

def increment_failed_attempts():
    attempts = get_failed_attempts() + 1
    with open(FAILED_ATTEMPTS_FILE, "w") as file:
        file.write(str(attempts))
    return attempts

def reset_failed_attempts():
    if os.path.exists(FAILED_ATTEMPTS_FILE):
        os.remove(FAILED_ATTEMPTS_FILE)

def self_destruct():
    import shutil
    if os.path.exists("data"):
        shutil.rmtree("data")  # Delete all stored data
    print("💀 System Self-Destructed! All notes erased. 💀")