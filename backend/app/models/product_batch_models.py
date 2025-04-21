from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship 
from database import Base

class ProductBatch(Base):
    __tablename__ = "product_batches"

    batch_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    expiry_date = Column(Date, nullable=False)
    received_date = Column(Date, nullable=False)

    product = relationship("Product", back_populates="batches")
