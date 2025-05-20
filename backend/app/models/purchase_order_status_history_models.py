from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone

class PurchaseOrderStatusHistory(Base):
    __tablename__ = "purchase_order_status_history"

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    status = Column(String(50), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    message = Column(String(100), nullable=True)

    purchase_order = relationship("PurchaseOrder", back_populates="status_history")