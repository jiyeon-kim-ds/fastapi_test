from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserSignup(UserBase):
    password: str


class UserSignin(UserSignup):
    pass
