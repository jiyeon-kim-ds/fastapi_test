from typing import Generator

from pydantic import BaseModel

from database.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Message(BaseModel):
    message: str
