import re

from passlib.context  import CryptContext


pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def get_password_hashed(password: str) -> str:
    return pwd_context.hash(password)


def validate_password(password: str) -> bool:
    if re.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
        return True
    return False
