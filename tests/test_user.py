import pytest

from core.auth       import get_password_hashed
from database.models import User
from tests.conftest  import client, TestingSessionLocal


db = TestingSessionLocal()


@pytest.fixture
def create_user():
    user_obj = User(
        username='existing_user@email.com',
        password=get_password_hashed('passWord123@')
    )

    db.add(user_obj)
    db.commit()

    yield

    db.delete(user_obj)
    db.commit()


existing_user_data = {
        "username": "existing_user@email.com",
        "password": "passWord123@"
    }


def test_create_user_success():
    signup_data = {
        "username": "testest@email.com",
        "password": "passWord123@"
    }
    response = client.post(
        "/user/signup",
        json=signup_data
    )
    assert response.status_code == 201


def test_create_user_wrong_password():
    signup_data = {
        "username": "wrong_password@email.com",
        "password": "password123"
    }
    response = client.post(
        "/user/signup",
        json=signup_data
    )
    assert response.status_code == 400


def test_create_existing_user(create_user):
    response = client.post(
        "/user/signup",
        json=existing_user_data
    )
    assert response.status_code == 409


def test_signin_success(create_user):
    response = client.post(
        "/user/signin",
        json=existing_user_data
    )

    assert response.status_code == 200, response.text['token']


def test_signin_fail(create_user):
    existing_user_data['password'] = 'wrong_password'

    response = client.post(
        "/user/signin",
        json=existing_user_data
    )

    assert response.status_code == 400
    