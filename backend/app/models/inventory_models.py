from sqlalchemy import Column, Integer, ForeignKey, Enum, TIMESTAMP, func
from database import Base
import enum

class TransactionTypeEnum(enum.Enum):
    sale = "sale"
    restock = "restock"

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    change_amount = Column(Integer, nullable=False)
    transaction_type = Column(Enum(TransactionTypeEnum), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    batch_id = Column(Integer, ForeignKey("product_batches.batch_id"))