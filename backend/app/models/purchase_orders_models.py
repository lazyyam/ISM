from sqlalchemy import Column, DateTime, Integer, ForeignKey, Date, String, DECIMAL, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from utils.timezone_config import MALAYSIA_TIMEZONE

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_date = Column(Date, default=lambda: datetime.now(MALAYSIA_TIMEZONE).date())
    status = Column(String(50), default="pending")
    total_cost = Column(DECIMAL(10, 2), default=0.00)
    description = Column(Text, nullable=True)
    payment_receipt_url = Column(String(255), nullable=True)
    payment_date = Column(DateTime, nullable=True)

    supplier = relationship("User", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")
    status_history = relationship("PurchaseOrderStatusHistory", back_populates="purchase_order", cascade="all, delete-orphan")