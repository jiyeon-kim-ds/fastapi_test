import re
from datetime import datetime, timedelta
from typing   import Any, Union

from fastapi         import Depends, status, Header, HTTPException, Request
from passlib.context import CryptContext
from sqlalchemy.orm  import Session
import jwt

from core.config  import settings
from routers.deps import get_db
from crud.user    import read_user_by_id
from core.config  import load_redis
from crud.ledger  import read_transaction_by_id


pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

JWT_ALGORITHM = "HS256"

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="무효한 토큰",
    headers={"WWW-Authenticate": "Bearer"},
)


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


def get_temp_user(
    token: str,
    url  : str,
    db   : Session = Depends(get_db)
):
    if 'transaction' not in url:
        raise credentials_exception

    req_transaction_id = int(url.split("/")[-1])

    r = load_redis(settings.temp_token_db)

    if not r.exists(token):
        raise credentials_exception

    ids = r.hgetall(token)

    user_id = int(ids['user_id'])
    transaction_id = int(ids['transaction_id'])

    if not read_transaction_by_id(transaction_id, user_id, db) or req_transaction_id != transaction_id:
        return False
    return user_id


def get_logged_in_user(
    request         : Request,
    authorization   : str | None = Header(default=None),
    db              : Session = Depends(get_db)
):
    token = request.query_params.get('token')

    if token:
        temp_user = get_temp_user(token, request.url.path, db)

        if temp_user:
            return read_user_by_id(temp_user, db)

    r = load_redis()

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
