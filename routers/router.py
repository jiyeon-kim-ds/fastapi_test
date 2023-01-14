from fastapi import APIRouter

from routers.user   import router as user_router
from routers.ledger import router as ledger_router


api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(ledger_router, prefix="/ledger", tags=["ledger"])
