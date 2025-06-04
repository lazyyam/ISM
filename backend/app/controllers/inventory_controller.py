from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models.inventory_models import Inventory
from schemas.inventory_schemas import InventoryRead
from typing import List

inventory_router = APIRouter()

@inventory_router.get("/", response_model=List[InventoryRead])
def get_inventory(db: Session = Depends(get_db)):
    inventory_entries = db.query(Inventory).options(joinedload(Inventory.product)).all()
    result = []
    for entry in inventory_entries:
        result.append({
            "id": entry.id,
            "product_id": entry.product_id,
            "change_amount": entry.change_amount,
            "transaction_type": entry.transaction_type,
            "created_at": entry.created_at,
            "batch_id": entry.batch_id,
            "product_name": entry.product.name if entry.product else "Unknown"
        })
    return result