from sqlalchemy.orm import Session

from database.models import Ledger
from schemas         import ledger as ledger_schema


def create_transaction(
    req_data: ledger_schema.TransactionCreate,
    db      : Session
) -> Ledger:
    transaction_dict = req_data.dict()

    transaction_obj = Ledger(**transaction_dict)

    db.add(transaction_obj)
    db.commit()
    db.refresh(transaction_obj)

    return transaction_obj


def read_transaction(
    transaction_id: int,
    user_id       : int,
    db            : Session
) -> Ledger:
    transaction = db.query(Ledger).filter(
            Ledger.id == transaction_id,
            Ledger.author_id == user_id
    )

    return transaction.first()


def update_transaction(
    transaction_id: int,
    req_data      : ledger_schema.TransactionUpdate,
    db            : Session
) -> Ledger:
    is_updated = db.query(Ledger).filter(Ledger.id == transaction_id).update(req_data.dict(exclude_unset=True))

    db.commit()

    return is_updated
