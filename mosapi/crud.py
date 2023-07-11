from sqlalchemy.orm import Session

from mosapi import database as models
from mosapi.schemas import entities


# Transactions
def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()


def get_transactions_by_account_name(db: Session, account_name: str, skip: int = 0, limit: int = 100):
    account = get_account_by_name(db, account_name=account_name)
    if account is None:
        return None

    return get_transactions_by_account(db, account_id=account.id, skip=skip, limit=limit)


def get_transactions_by_account(db: Session, account_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).filter(models.Transaction.account_id == account_id).offset(skip).limit(limit).all()


def add_transaction(db: Session, transaction: entities.TransactionCreate, account_id: int):
    db_transaction = models.Transaction(
        **transaction.dict(), account_id=account_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


def add_transaction_to_account_name(db: Session, transaction: entities.TransactionCreate, account_name: str):
    """We may use account id, but whateverGPT may not be that powerful."""
    account = get_account_by_name(db, account_name)
    db_transaction = models.Transaction(
        **transaction.dict(), account_id=account.id_)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


# Accounts
def get_accounts(db: Session):
    return db.query(models.Account).all()


def get_account_by_id(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id_ == account_id).first()


def get_account_by_name(db: Session, account_name: str):
    return db.query(models.Account).filter(models.Account.name == account_name).first()


def create_account_if_missing(db: Session, account: entities.AccountCreate):
    existing_account = get_account_by_name(db, account.name)

    if existing_account:
        return existing_account

    new_account = models.Account(name=account.name, number=account.number)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account
