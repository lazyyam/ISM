from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


#PURCHASE_ORDER_ITEM
class PurchaseOrderItemBase(BaseModel):
    supplier_product_id: int
    quantity: int
    unit_cost: float
    subtotal: float

    class Config:
        orm_mode = True

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItemRead(PurchaseOrderItemBase):
    id: int

    class Config:
        orm_mode = True


#PURCHASE_ORDER
class PurchaseOrderBase(BaseModel):
    supplier_id: int
    status: Optional[str] = "pending"
    total_cost: Optional[float] = 0.00

class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderItemCreate]
    description: Optional[str] = None

class PurchaseOrderRead(PurchaseOrderBase):
    id: int
    order_date: datetime
    items: List[PurchaseOrderItemRead]
    supplier_name: str
    company_name: str
    description: Optional[str] = None
    supplier_name: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        orm_mode = True

class PurchaseOrderStatusUpdate(BaseModel):
    status: str