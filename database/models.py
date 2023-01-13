from sqlalchemy     import Column, Datetime, String, Integer, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class PrimaryKey:
    id = Column(Integer, primary_key=True, index=True, unique=True)


class User(Base, PrimaryKey):
    __tablename__ = 'users'

    username    = Column(String(255), nullable=False, unique=True)
    password    = Column(String(255), nullable=False)
    joined_date = Column(DateTime(), server_default=func.now())
