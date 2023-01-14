from typing   import Optional, Union
from datetime import datetime

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    author_id : Optional[int]
    item      : Optional[str]
    note      : Optional[str]
    amount    : int
    event_date: Union[str, datetime]
