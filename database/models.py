from sqlalchemy     import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class PrimaryKey(Base):
    id = Column(Integer, primary_key=True, unique=True)


class User(PrimaryKey):
    __tablename__ = 'users'

    username    = Column(String(255), nullable=False, unique=True)
    password    = Column(String(255), nullable=False)
    joined_date = Column(DateTime(), server_default=func.now())
    ledgers     = relationship('Ledger', back_populates='author')


class Ledger(PrimaryKey):
    __tablename__ = 'ledgers'

    author_id  = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    author     = relationship('User', back_populates='ledgers')
    item       = Column(String(255))
    note       = Column(Text())
    amount     = Column(Integer(), nullable=False)
    event_date = Column(DateTime())  # 거래 발생 날짜
    created_at = Column(DateTime(), server_default=func.now())  # ledger 생성 날짜
