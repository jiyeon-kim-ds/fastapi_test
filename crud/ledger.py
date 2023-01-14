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
