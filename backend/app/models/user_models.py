from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.utils.timezone_config import MALAYSIA_TIMEZONE

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(80), nullable=False)
    full_name = Column(String(50), nullable=False)
    role = Column(String(10))
    phone_number = Column(String(20), nullable=False)
    company_name = Column(String(100), nullable=True)
    company_address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(MALAYSIA_TIMEZONE))

    supplier_products = relationship("SupplierProduct", back_populates="supplier", cascade="all, delete-orphan")
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier", cascade="all, delete-orphan")
    bank_accounts = relationship("SupplierBankAccount", back_populates="supplier", cascade="all, delete-orphan")