from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProductMapping(Base):
    __tablename__ = "product_mapping"

    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    supplier_product_id = Column(Integer, ForeignKey("supplier_products.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    supplier = relationship("User")
    supplier_product = relationship("SupplierProduct")
    product = relationship("Product")