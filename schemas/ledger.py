from typing   import Optional, Union, List
from datetime import datetime

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    author_id : Optional[int]
    item_name : Optional[str]
    note      : Optional[str]
    amount    : int
    event_date: Union[str, datetime]


class TransactionUpdate(BaseModel):
    author_id : Optional[int]
    item_name : Optional[str]
    note      : Optional[str]
    amount    : Optional[int]
    event_date: Union[str, datetime]


class TransactionBulkDelete(BaseModel):
    ledger_ids: List[int]
