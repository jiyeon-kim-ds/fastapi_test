from fastapi           import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm    import Session

from core.auth       import (
    get_password_hashed,
    validate_password,
    verify_password,
    create_access_token,
)
from crud            import user as user_crud
from routers.deps    import get_db, Message
from schemas         import user as user_schema


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

    if not validate_password(password):
        return JSONResponse(status_code=400, content={"message": "비밀번호 조건 불만족"})

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
