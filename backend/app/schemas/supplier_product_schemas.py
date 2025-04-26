from datetime import datetime
from typing import Optional
from pydantic import BaseModel 


class SupplierProductBase(BaseModel):
    name: str
    category: str
    code: str
    cost: float
    quantity_available: int

class SupplierProductCreate(SupplierProductBase):
    pass

class SupplierProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    cost: Optional[float] = None
    quantity_available: Optional[int] = None

class SupplierProductRead(SupplierProductBase):
    id: int
    supplier_id: int
    created_at: datetime

    class Config:
        orm_mode = True