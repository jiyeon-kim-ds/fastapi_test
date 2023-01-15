from sqlalchemy     import Column, String, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func, expression

Base = declarative_base()


class PrimaryKey:
    id = Column(Integer, primary_key=True, unique=True)


class User(Base, PrimaryKey):
    __tablename__ = 'users'

    username    = Column(String(255), nullable=False, unique=True)
    password    = Column(String(255), nullable=False)
    joined_date = Column(DateTime(), server_default=func.now())
    ledgers     = relationship('Ledger', back_populates='author')


class Ledger(Base, PrimaryKey):
    __tablename__ = 'ledgers'

    author_id  = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    author     = relationship('User', back_populates='ledgers')
    item_name  = Column(String(255))
    note       = Column(Text())
    amount     = Column(Integer(), nullable=False)
    event_date = Column(DateTime())  # 거래 발생 날짜
    created_at = Column(DateTime(), server_default=func.now())  # ledger 생성 날짜
    is_deleted = Column(Boolean(), server_default=expression.false())
