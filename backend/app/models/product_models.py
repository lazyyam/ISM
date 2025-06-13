from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    cost = Column(DECIMAL(10, 2), nullable=False)
    retail_price = Column(DECIMAL(10, 2), nullable=False)
    stock_threshold = Column(Integer, nullable=False)

    batches = relationship("ProductBatch", back_populates="product", cascade="all, delete-orphan")
    inventory = relationship("Inventory", back_populates="product", cascade="all, delete-orphan")

    