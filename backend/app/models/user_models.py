from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, timezone
from database import Base

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
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
