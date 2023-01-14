from tests.conftest  import client, TestingSessionLocal


db = TestingSessionLocal()


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


def test_create_existing_user():
    response = client.post(
        "/user/signup",
        json=existing_user_data
    )
    assert response.status_code == 409


def test_signin_success():
    response = client.post(
        "/user/signin",
        json=existing_user_data
    )

    assert response.status_code == 200, response.text['token']


def test_signin_fail():
    existing_user_data['password'] = 'wrong_password'

    response = client.post(
        "/user/signin",
        json=existing_user_data
    )

    assert response.status_code == 400
    