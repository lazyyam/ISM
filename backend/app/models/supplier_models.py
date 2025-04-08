from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    company_name = Column(String(100), nullable=False)
    company_address = Column(String(200))

    user = relationship("User", back_populates="supplier")