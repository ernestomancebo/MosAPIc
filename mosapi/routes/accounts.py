from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mosapi import crud
from mosapi.database import get_database
from mosapi.schemas import entities

router = APIRouter(prefix="/accounts",
                   tags=["accounts"],
                   responses={404: {"description": "Not found"}})


@router.get("/info")
async def root():
    return {"response": "Accounts Route"}


@router.get("/", response_model=list[entities.Account])
async def get_all_accounts(db: Session = Depends(get_database)):
    accounts = crud.get_accounts(db)
    return accounts


@router.get("/{account_name}", response_model=entities.Account)
async def get_by_account_name(account_name: str, db: Session = Depends(get_database)):
    account = crud.get_account_by_name(db, account_name=account_name)
    if account is None:
        return HTTPException(404, f"Account with account name '{account_name}' was not found.")

    return account


@router.get("/{account_id}", response_model=entities.Account)
async def get_by_account_id(account_id: int, db: Session = Depends(get_database)):
    account = crud.get_account_by_id(db, account_id=account_id)
    if account is None:
        return HTTPException(404, f"Account with account ID '{account_id}' was not found.")

    return account
