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


@router.post("", status_code=status.HTTP_201_CREATED, responses=authentication_responses)
def post_transaction(
    transaction_data: ledger_schema.TransactionCreate,
    user            : User = Depends(get_logged_in_user),
    db               : Session = Depends(get_db)
):
    transaction_data.author_id = user.id
    transaction_data.event_date = datetime.strptime(transaction_data.event_date, '%Y-%m-%d')

    ledger_crud.create_transaction(transaction_data, db)

    return JSONResponse(status_code=201, content={"message": "내역 생성 성공"})
