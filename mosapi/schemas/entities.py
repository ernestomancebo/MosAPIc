from random import choice

from pydantic import BaseModel, constr
from pydantic_factories import Ignore, ModelFactory, Use


# Transactions related
class TransactionBase(BaseModel):
    description: constr(max_length=150)
    amount: float
    transaction_type: constr(max_length=20)
    account_id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionFactory(ModelFactory[TransactionCreate]):
    __model__ = TransactionCreate

    transaction_type = Use(choice, ['debit', 'credit'])
    # Need to be skip
    # account_id = Ignore()


class Transaction(TransactionBase):
    id_: int

    class Config:
        orm_mode = True


# Account related
class AccountBase(BaseModel):
    name: str
    number: int


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id_: int
    transactions: list[Transaction] = []

    class Config:
        orm_mode = True
