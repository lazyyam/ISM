from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


#PURCHASE_ORDER_STATUS_HISTORY
class StatusHistoryEntry(BaseModel):
    status: str
    updated_at: datetime
    message: Optional[str] = None


#PURCHASE_ORDER_ITEM
class PurchaseOrderItemBase(BaseModel):
    supplier_product_id: int
    quantity: int
    unit_cost: float
    subtotal: float

    class Config:
        from_attributes = True

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItemRead(PurchaseOrderItemBase):
    id: int
    product_name: Optional[str] = None

    class Config:
        from_attributes = True


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
    order_date: str
    items: List[PurchaseOrderItemRead]
    description: Optional[str] = None
    supplier_name: Optional[str] = None
    company_name: Optional[str] = None
    status_history: Optional[List[StatusHistoryEntry]] = []

    class Config:
        from_attributes = True

class PurchaseOrderStatusUpdate(BaseModel):
    status: str
    message: Optional[str] = None