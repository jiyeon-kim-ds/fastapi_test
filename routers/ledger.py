from datetime import datetime

from fastapi           import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm    import Session

from core.auth       import get_logged_in_user
from crud            import ledger as ledger_crud
from routers.deps    import get_db, Message
from schemas         import ledger as ledger_schema
from database.models import User


router = APIRouter()


authentication_responses = {
    401: {"model": Message, "description": "무효한 토큰"},
}

ledger_responses = {
    401: {"model": Message, "description": "무효한 토큰"},
    404: {"model": Message, "description": "거래 내역 없음"},
}


@router.post("/transaction", status_code=status.HTTP_201_CREATED, responses=authentication_responses)
def post_transaction(
    transaction_data: ledger_schema.TransactionCreate,
    user            : User = Depends(get_logged_in_user),
    db               : Session = Depends(get_db)
):
    transaction_data.author_id = user.id
    transaction_data.event_date = datetime.strptime(transaction_data.event_date, '%Y-%m-%d %H:%M:%S.%f')

    ledger_crud.create_transaction(transaction_data, db)

    return JSONResponse(status_code=201, content={"message": "내역 생성 성공"})


@router.patch("/transaction/{transaction_id}", status_code=status.HTTP_200_OK, responses=ledger_responses)
def patch_transaction(
    transaction_id  : int,
    transaction_data: ledger_schema.TransactionUpdate,
    user            : User = Depends(get_logged_in_user),
    db              : Session = Depends(get_db)
):
    transaction = ledger_crud.read_transaction(transaction_id, user.id, db)

    if not transaction:
        return JSONResponse(status_code=404, content={"message": "내역 없음"})

    transaction_data.event_date = datetime.strptime(transaction_data.event_date, '%Y-%m-%d %H:%M:%S.%f')
    is_updated = ledger_crud.update_transaction(transaction.id, transaction_data, db)

    return is_updated
