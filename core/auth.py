import re
from datetime import datetime, timedelta
from typing   import Any, Union

from fastapi             import Depends, status, Header
from passlib.context     import CryptContext
from sqlalchemy.orm      import Session
from starlette.responses import JSONResponse
import jwt

from core.config  import settings
from routers.deps import get_db
from crud.user    import read_user_by_id


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
    credentials_exception = JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content="무효한 토큰",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not authorization:
        raise credentials_exception

    try:
        payload = jwt.decode(authorization, settings.auth_secret, algorithms=JWT_ALGORITHM)
    except jwt.ExpiredSignatureError:
        return credentials_exception
    except jwt.InvalidTokenError:
        return credentials_exception

    user_id = payload.get("sub")

    user = read_user_by_id(user_id, db)

    return user
