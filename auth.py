from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOCKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

def hash_password(password:str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, password_hash)

def create_access_token(username:str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOCKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "exp": ACCESS_TOCKEN_EXPIRE_MINUTES
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)