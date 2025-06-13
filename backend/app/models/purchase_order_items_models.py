from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base

class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"

    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    supplier_product_id = Column(Integer, ForeignKey("supplier_products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)

    purchase_order = relationship("PurchaseOrder", back_populates="items")
    supplier_product = relationship("SupplierProduct", back_populates="order_items")
