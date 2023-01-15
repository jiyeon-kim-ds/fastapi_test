from typing   import List
from datetime import datetime, timedelta

from sqlalchemy     import func
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


def read_transaction_by_id(
    transaction_id: int,
    user_id       : int,
    db            : Session
) -> Ledger:
    transaction = db.query(Ledger).filter(
            Ledger.id == transaction_id,
            Ledger.author_id == user_id,
            Ledger.is_deleted.is_(False),
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


def read_ledger(
    user_id: int,
    db     : Session
) -> List[Ledger]:
    ledger = db.query(Ledger).filter(
        Ledger.author_id == user_id, Ledger.is_deleted.is_(False)
    ).order_by(Ledger.event_date.desc)

    return ledger.all()


def delete_bulk_ledger(
    ledger_data: ledger_schema.TransactionBulkDelete,
    user_id    : int,
    db         : Session
):
    is_deleted = db.query(Ledger).where(
                Ledger.id.in_(ledger_data.ledger_ids),
                Ledger.author_id == user_id
            ).update({"is_deleted": True})

    db.commit()

    return is_deleted


def read_total_amount(
    user_id   : int,
    db        : Session,
    start_date: datetime = datetime.strptime("1990-01-01", "%Y-%m-%d"),
    end_date  : datetime = datetime.today() + timedelta(days=1),
) -> Ledger:
    total_amount = db.query(Ledger).with_entities(
        func.sum(Ledger.amount).label("total_amount")
    ).filter(
        Ledger.author_id == user_id,
        Ledger.is_deleted.is_(False),
        Ledger.event_date.between(start_date, end_date)
    )

    return total_amount.first()
