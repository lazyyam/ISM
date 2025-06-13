from sqlalchemy import Column, Integer, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    sell_date = Column(Date, nullable=False)
    remarks = Column(Text, nullable=True)

    product = relationship("Product")