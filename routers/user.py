from fastapi           import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm    import Session

from core.auth    import get_password_hashed, validate_password
from crud         import user as user_crud
from routers.deps import get_db, Message
from schemas      import user as user_crud


router = APIRouter()


signup_responses = {
    409: {"model": Message, "description": "중복된 username"},
    400: {"model": Message, "description": "비밀번호 조건 불만족"}
}


@router.post("/signup", status_code=status.HTTP_201_CREATED, responses=signup_responses)
def signup(
    signup_data: user_crud.UserSignup,
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


@router.post("signin", status_code=status.HTTP_200_OK)
def signin(
    signin_data: user_crud.UserSignin,
    db         : Session = Depends(get_db)
):
    pass