from datetime import datetime

from tests.conftest  import client, get_user_token


token_header = get_user_token()


def test_create_ledger():
    ledger_data = {
        "item": "꽤나 큰 지출",
        "note": "너무 큰 지출을 해버렸다!",
        "amount": -1000000,
        "event_date": str(datetime.now().date())
    }

    response = client.post(
        "/ledger",
        json=ledger_data,
        headers=token_header
    )

    assert response.status_code == 201
