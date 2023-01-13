from sqlalchemy.orm import Session

from database.models import User
from schemas.user    import UserSignup


def read_user(
    req_username: str,
    db: Session
) -> User:
    user = db.query(User).filter(User.username == req_username)

    return user.first()


def create_user(
    signup_data: UserSignup,
    db: Session
) -> User:
    user_obj = User(
        username = signup_data.username,
        password = signup_data.password
    )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return user_obj
