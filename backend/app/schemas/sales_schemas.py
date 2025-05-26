from pydantic import BaseModel
from typing import Optional
from datetime import date

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    sell_date: date
    remarks: Optional[str] = None

class SaleCreate(SaleBase):
    pass

class SaleRead(SaleBase):
    id: int

    class Config:
        from_attributes = True