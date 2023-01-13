import re
from datetime import datetime, timedelta
from typing   import Any, Union

from passlib.context import CryptContext
import jwt

from core.config import settings


pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

JWT_ALGORITHM = "HS256"


def get_password_hashed(password: str) -> str:
    return pwd_context.hash(password)


def validate_password(password: str) -> bool:
    if re.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
        return True
    return False


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: Union[str, Any]
)-> str:
    expiry = datetime.utcnow() + timedelta(days=7)
    encoded = jwt.encode(
        payload={'exp': expiry,
                 'sub': str(subject)},
        key=settings.auth_secret,
        algorithm=JWT_ALGORITHM
    )

    return encoded
