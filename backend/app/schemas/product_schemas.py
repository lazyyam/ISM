from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

#INVENTORY
class TransactionTypeEnum(str, Enum):
    sale = "sale"
    restock = "restock"

class InventoryBase(BaseModel):
    product_id: int
    change_amount: int
    transaction_type: TransactionTypeEnum
    batch_id: Optional[int] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryRead(InventoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


#PRODUCT_BATCH
class ProductBatchBase(BaseModel):
    product_id: int
    quantity: int
    expiry_date: date

class ProductBatchCreate(ProductBatchBase):
    pass

class ProductBatchRead(ProductBatchBase):
    batch_id: int
    received_date: datetime

    class Config:
        orm_mode = True


#PRODUCT
class ProductBase(BaseModel):
    name: str
    category: str
    code: str
    cost: float
    retail_price: float
    stock_threshold: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    batches: List[ProductBatchRead] = []
    inventory: List[InventoryRead] = []

    class Config:
        orm_mode = True
