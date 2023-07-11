from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'
    id_ = Column(Integer, name='id', primary_key=True, index=True)
    description = Column(String(150), nullable=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(20), nullable=False)
    """Debit or Credit"""
    transaction_date = Column(DateTime(timezone=True),
                              server_default=func.now())
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship('Account', back_populates='transactions')


class Account(Base):
    __tablename__ = 'accounts'
    id_ = Column(Integer, name='id', primary_key=True, index=True)
    name = Column(String(25), nullable=False)
    number = Column(Integer, nullable=False)
    creation_date = Column(DateTime(timezone=True),
                           server_default=func.now())

    transactions = relationship("Transaction", back_populates="account")


def get_database():
    """For Dependency Injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
