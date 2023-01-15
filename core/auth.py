import re
from datetime import datetime, timedelta
from typing   import Any, Union
from random   import choice
from string   import ascii_letters

from fastapi         import Depends, status, Header, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm  import Session
import jwt

from core.config  import settings
from routers.deps import get_db
from crud.user    import read_user_by_id
from core.config  import load_redis


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
) -> str:
    expiry = datetime.utcnow() + timedelta(days=7)
    encoded = jwt.encode(
        payload={'exp': expiry,
                 'sub': str(subject)},
        key=settings.auth_secret,
        algorithm=JWT_ALGORITHM
    )

    return encoded


def get_logged_in_user(
    authorization: str | None = Header(default=None),
    db           : Session = Depends(get_db)
):
    r = load_redis()

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="무효한 토큰",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not authorization or r.exists(authorization):
        raise credentials_exception

    try:
        payload = jwt.decode(authorization, settings.auth_secret, algorithms=JWT_ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    user_id = payload.get("sub")

    user = read_user_by_id(user_id, db)

    return user


def create_temp_token(
    transaction_id: int,
    user_id       : int
):
    temp_token = ''.join(choice(ascii_letters) for i in range(16))

    r = load_redis(settings.temp_token_db)
    r.setex(temp_token, timedelta(minutes=30), value=user_id)

    return temp_token




def get_temp_user():
