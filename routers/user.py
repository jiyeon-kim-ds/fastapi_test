from datetime import timedelta

from fastapi           import APIRouter, Depends, status, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm    import Session

from core.auth       import (
    get_password_hashed,
    validate_password,
    verify_password,
    create_access_token,
    get_logged_in_user,
    validate_email
)
from crud            import user as user_crud
from routers.deps    import get_db, Message
from schemas         import user as user_schema
from core.config     import load_redis
from database.models import User
from routers.ledger  import authentication_responses


router = APIRouter()


signup_responses = {
    400: {"model": Message, "description": "비밀번호 조건 불만족"},
    409: {"model": Message, "description": "중복된 username"},
}

signin_responses = {
    400: {"model": Message, "description": "사용자 정보 불일치"}
}


@router.post("/signup", status_code=status.HTTP_201_CREATED, responses=signup_responses)
def post_user_signup(
    signup_data: user_schema.UserSignup,
    db         : Session = Depends(get_db)
):
    duplicate_user = user_crud.read_user(signup_data.username, db)

    if duplicate_user:
        return JSONResponse(status_code=409, content={"message": "중복된 username"})

    password = signup_data.password

    if not validate_password(password) or not validate_email(signup_data.username):
        return JSONResponse(status_code=400, content={"message": "이메일 및 비밀번호 조건 불만족"})

    signup_data.password = get_password_hashed(password)

    user_crud.create_user(signup_data, db)

    return JSONResponse(status_code=201, content={"message": "회원가입 성공"})


@router.post("/signin", status_code=status.HTTP_200_OK, responses=signin_responses)
def post_user_signin(
    signin_data: user_schema.UserSignin,
    db         : Session = Depends(get_db)
):
    user = user_crud.read_user(signin_data.username, db)

    if not user or not verify_password(signin_data.password, user.password):
        return JSONResponse(status_code=400, content={"message": "사용자 정보 불일치"})

    return {'token': create_access_token(user.id)}


@router.post("/signout", status_code=204, responses=authentication_responses)
def post_user_signout(
    authorization: str | None = Header(default=None),
    user         : User = Depends(get_logged_in_user),
):
    r = load_redis()

    r.setex(authorization, timedelta(days=7), value=user.id)
