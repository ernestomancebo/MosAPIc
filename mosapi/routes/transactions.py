from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mosapi import crud
from mosapi.database import get_database
from mosapi.schemas import entities

router = APIRouter(prefix="/transactions",
                   tags=["transactions"],
                   responses={404: {"description": "Not found"}})


@router.get("/info")
async def root():
    return {"response": "Accounts Route"}


@router.get("/", response_model=list[entities.Transaction])
async def get_all_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    transactions = crud.get_transactions(db, skip=skip, limit=limit)
    return transactions


@router.get("/{account_name}", response_model=list[entities.Transaction])
async def get_by_account_name(account_name: str, db: Session = Depends(get_database)):
    account = crud.get_transactions_by_account_name(
        db, account_name=account_name)
    if account is None:
        return HTTPException(404, f"Transactions with account name '{account_name}' was not found.")

    return account


@router.get("/{account_id}", response_model=entities.Account)
async def get_by_account_id(account_id: int, db: Session = Depends(get_database)):
    account = crud.get_transactions_by_account(db, account_id=account_id)
    if account is None:
        return HTTPException(404, f"Transactions with account ID '{account_id}' was not found.")

    return account
