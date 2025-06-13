from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from app.utils.timezone_config import MALAYSIA_TIMEZONE

class PurchaseOrderStatusHistory(Base):
    __tablename__ = "purchase_order_status_history"

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    status = Column(String(50), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(MALAYSIA_TIMEZONE))
    message = Column(String(100), nullable=True)

    purchase_order = relationship("PurchaseOrder", back_populates="status_history")