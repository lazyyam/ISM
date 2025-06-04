from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class TransactionTypeEnum(str, Enum):
    sale = "sale"
    restock = "restock"
    manual_add = "manual_add"
    adjustment = "adjustment"

class InventoryBase(BaseModel):
    product_id: int
    change_amount: int
    transaction_type: TransactionTypeEnum
    batch_id: Optional[int] = None

class InventoryRead(InventoryBase):
    id: int
    created_at: datetime
    product_name: Optional[str] = None 
    batch_id: Optional[int] = None

    class Config:
        from_attributes = True