from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, DECIMAL
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_date = Column(DateTime, default=datetime.now(timezone.utc))
    status = Column(String(50), default="pending")
    total_cost = Column(DECIMAL(10, 2), default=0.00)

    supplier = relationship("User", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")
