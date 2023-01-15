from datetime import datetime

import pytest

from tests.conftest  import client, get_user_token, TestingSessionLocal, get_user_by_id, get_transaction
from database.models import Ledger


token_header = get_user_token()
db = TestingSessionLocal()


@pytest.fixture(scope='module', autouse=True)
def create_transaction():
    user = get_user_by_id()

    transaction_obj = Ledger(
        author_id =user.id,
        item_name ="테스트 아이템",
        note      ="테스트 노트",
        amount    =1000000,
        event_date=datetime.today(),
    )

    db.add(transaction_obj)
    db.commit()


def test_create_transaction():
    transaction_data = {
        "item_name" : "꽤나 큰 지출",
        "note"      : "너무 큰 지출을 해버렸다!",
        "amount"    : -1000000,
        "event_date": str(datetime.now())
    }

    response = client.post(
        "/ledger/transaction",
        json=transaction_data,
        headers=token_header
    )

    assert response.status_code == 201


def test_update_transaction():
    transaction_data = {
        "item_name": "꽤나 작은 지출",
        "amount": -1000,
        "event_date": str(datetime.now())
    }

    transaction = get_transaction()

    response = client.patch(
        f"/ledger/transaction/{transaction.id}",
        json=transaction_data,
        headers=token_header
    )

    assert response.status_code == 200


def test_copy_transaction():
    transaction = get_transaction()

    response = client.post(
        f"/ledger/transaction/{transaction.id}",
        headers=token_header
    )

    assert response.status_code == 201


def test_read_transaction():
    transaction = get_transaction()

    response = client.get(
        f"/ledger/transaction/{transaction.id}",
        headers=token_header
    )

    assert response.status_code == 200


def test_read_ledger():
    response = client.get(
        "/ledger",
        headers=token_header
    )

    assert response.status_code == 200


def test_delete_ledger():
    transaction = get_transaction()

    ledger_data = {"ledger_ids": [transaction.id, 10000]}

    response = client.patch(
        "/ledger/transaction",
        json=ledger_data,
        headers=token_header
    )

    assert response.status_code == 204
