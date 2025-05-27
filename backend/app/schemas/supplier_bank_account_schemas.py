from pydantic import BaseModel

class SupplierBankAccountBase(BaseModel):
    bank_name: str
    account_number: str
    account_holder: str

class SupplierBankAccountCreate(SupplierBankAccountBase):
    pass

class SupplierBankAccountRead(SupplierBankAccountBase):
    id: int
    supplier_id: int

    class Config:
        from_attributes = True