from fastapi.testclient import TestClient
from sqlalchemy         import create_engine
from sqlalchemy.orm     import sessionmaker
import pytest

from main            import app
from routers.deps    import get_db
from database.models import Base, User, Ledger
from core.auth       import get_password_hashed, create_access_token


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
db = TestingSessionLocal()


@pytest.fixture(scope='session', autouse=True)
def create_user():
    user_obj = User(
        username='existing_user@email.com',
        password=get_password_hashed('passWord123@')
    )

    db.add(user_obj)
    db.commit()


def get_user_token():
    user_obj = User(
        username='token@email.com',
        password=get_password_hashed('passWord123@')
    )

    db.add(user_obj)
    db.commit()

    db.refresh(user_obj)

    return {"Authorization": create_access_token(user_obj.id)}


def get_user_by_id():
    user = db.query(User).filter(User.username == "token@email.com").first()

    return user


def get_transaction():
    user = get_user_by_id()

    ledger = db.query(Ledger.id).filter(Ledger.author_id == user.id).first()

    return ledger
