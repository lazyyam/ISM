from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models.purchase_orders_models import PurchaseOrder
from models.purchase_order_items_models import PurchaseOrderItem
from schemas.purchase_order_schemas import PurchaseOrderCreate, PurchaseOrderRead, PurchaseOrderItemCreate
from typing import List

purchase_order_router = APIRouter()


# Get all Purchase Orders with their Items
@purchase_order_router.get("/", response_model=List[PurchaseOrderRead])
def get_purchase_orders(db: Session = Depends(get_db)):
    purchase_orders = db.query(PurchaseOrderRead).options(
        joinedload(PurchaseOrderRead.items)
    ).all()
    return purchase_orders


# Create a Purchase Order with Items
@purchase_order_router.post("/", response_model=PurchaseOrderRead)
def create_purchase_order(order_data: PurchaseOrderCreate, db: Session = Depends(get_db)):
    new_order = PurchaseOrderRead(
        supplier_id=order_data.supplier_id,
        status=order_data.status,
        total_cost=order_data.total_cost
    )
    db.add(new_order)
    db.flush()  # So that new_order.id is available

    # Create PurchaseOrderItems linked to the new_order
    for item_data in order_data.items:
        new_item = PurchaseOrderItem(
            purchase_order_id=new_order.id,
            supplier_product_id=item_data.supplier_product_id,
            quantity=item_data.quantity,
            unit_cost=item_data.unit_cost,
            subtotal=item_data.subtotal
        )
        db.add(new_item)

    db.commit()
    db.refresh(new_order)
    return new_order


# Update Purchase Order (status, total cost)
@purchase_order_router.put("/{order_id}", response_model=PurchaseOrderRead)
def update_purchase_order(order_id: int, updated_data: PurchaseOrderCreate, db: Session = Depends(get_db)):
    order = db.query(PurchaseOrderRead).filter(PurchaseOrderRead.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Purchase Order not found")

    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order


# Delete Purchase Order (and cascade delete its Items)
@purchase_order_router.delete("/{order_id}")
def delete_purchase_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(PurchaseOrderRead).filter(PurchaseOrderRead.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Purchase Order not found")

    db.delete(order)
    db.commit()
    return {"detail": "Purchase Order and its items deleted successfully"}
