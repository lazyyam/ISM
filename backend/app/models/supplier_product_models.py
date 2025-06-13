from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from app.utils.timezone_config import MALAYSIA_TIMEZONE

class SupplierProduct(Base):
    __tablename__ = "supplier_products"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    cost = Column(DECIMAL(10, 2), nullable=False)
    quantity_available = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(MALAYSIA_TIMEZONE))

    supplier = relationship("User", back_populates="supplier_products")
    order_items = relationship("PurchaseOrderItem", back_populates="supplier_product")
