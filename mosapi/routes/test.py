from faker import Faker
# from faker.providers.lorem import Provider
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from mosapi import crud
from mosapi.database import get_database
from mosapi.schemas import entities
from random import randint
router = APIRouter(prefix="/test",
                   tags=["test"],
                   responses={404: {"description": "Not found"}})

Faker.seed(25)

ACCOUNTS = ['ASSETS', 'LIABILITIES', 'EXPENSES', 'INCOMES',
            'ACCOUNTS PAYABLES', 'REVENUE', 'ACCOUNTS RECEIVABLE']


@router.get("/")
async def root():
    return {"response": "Test Route"}


@router.post("/create-accounts", response_model=list[entities.Account])
async def create_accounts(db: Session = Depends(get_database)):
    accounts = []
    for number, name in enumerate(ACCOUNTS):
        account_create = entities.AccountCreate(name=name, number=number)
        accounts.append(crud.create_account_if_missing(db, account_create))

    return accounts


@router.post("/add-random-transactions", response_model=list[entities.Transaction])
async def add_random_transactions(db: Session = Depends(get_database)):
    new_transactions = []
    faker = Faker()
    for account_name in ACCOUNTS:
        account = crud.get_account_by_name(db, account_name)
        transactions = entities.TransactionFactory.batch(size=randint(3, 8))

        for t in transactions:
            # Some dirty job
            t.description = faker.text(max_nb_chars=50)
            t.__delattr__('account_id')
            # Good to go
            new_transactions.append(crud.add_transaction(db,
                                                         transaction=t,
                                                         account_id=account.id_))

    return new_transactions
