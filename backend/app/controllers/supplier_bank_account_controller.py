from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.auth_dependencies import get_current_user
from app.database import get_db
from app.models.supplier_bank_account_models import SupplierBankAccount
from app.schemas.supplier_bank_account_schemas import SupplierBankAccountCreate, SupplierBankAccountRead
from typing import List

supplier_bank_account_router = APIRouter()

@supplier_bank_account_router.get("/by-supplier", response_model=List[SupplierBankAccountRead])
def get_bank_accounts_by_supplier(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(SupplierBankAccount).filter(SupplierBankAccount.supplier_id == current_user.id).all()

@supplier_bank_account_router.get("/by-supplier/{supplier_id}", response_model=List[SupplierBankAccountRead])
def get_bank_accounts_by_supplier_id(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    return db.query(SupplierBankAccount).filter(SupplierBankAccount.supplier_id == supplier_id).all()

@supplier_bank_account_router.post("/", response_model=SupplierBankAccountRead)
def create_or_update_bank_account(
    bank_account: SupplierBankAccountCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    existing = db.query(SupplierBankAccount).filter(SupplierBankAccount.supplier_id == current_user.id).first()
    if existing:
        # Update existing bank account
        existing.bank_name = bank_account.bank_name
        existing.account_number = bank_account.account_number
        existing.account_holder = bank_account.account_holder
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Create new bank account
        new_account = SupplierBankAccount(
            supplier_id=current_user.id,
            **bank_account.model_dump()
        )
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_account

@supplier_bank_account_router.delete("/{account_id}")
def delete_bank_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(SupplierBankAccount).filter(SupplierBankAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    db.delete(account)
    db.commit()
    return {"detail": "Bank account deleted"}