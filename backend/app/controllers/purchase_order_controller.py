from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models.purchase_orders_models import PurchaseOrder
from models.purchase_order_items_models import PurchaseOrderItem
from schemas.purchase_order_schemas import PurchaseOrderCreate, PurchaseOrderRead, PurchaseOrderItemCreate, PurchaseOrderStatusUpdate
from typing import List

purchase_order_router = APIRouter()


# Get all Purchase Orders with their Items
@purchase_order_router.get("/", response_model=List[PurchaseOrderRead])
def get_purchase_orders(db: Session = Depends(get_db)):
    purchase_orders = db.query(PurchaseOrder).options(
        joinedload(PurchaseOrder.supplier)
    ).all()

    response = []
    for order in purchase_orders:
        response.append({
            "id": order.id,
            "order_date": order.order_date,
            "supplier_id": order.supplier_id,
            "supplier_name": order.supplier.full_name if order.supplier else None,
            "company_name": order.supplier.company_name if order.supplier else None,
            "description": order.description,
            "status": order.status,
            "total_cost": order.total_cost,
            "items": [
                {
                    "id": item.id,
                    "supplier_product_id": item.supplier_product_id,
                    "quantity": item.quantity,
                    "unit_cost": item.unit_cost,
                    "subtotal": item.subtotal,
                }
                for item in order.items
            ],
        })

    return response



# Create a Purchase Order with Items
@purchase_order_router.post("/", response_model=PurchaseOrderRead)
def create_purchase_order(order_data: PurchaseOrderCreate, db: Session = Depends(get_db)):
    new_order = PurchaseOrder(
        supplier_id=order_data.supplier_id,
        status=order_data.status,
        total_cost=order_data.total_cost,
        description=order_data.description
    )
    db.add(new_order)
    db.flush()  # Make sure new_order.id is available for FK

    # Add items
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


# Update Purchase Order
@purchase_order_router.put("/{order_id}", response_model=PurchaseOrderRead)
def update_purchase_order(order_id: int, updated_data: PurchaseOrderCreate, db: Session = Depends(get_db)):
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Purchase Order not found")

    order.supplier_id = updated_data.supplier_id
    order.status = updated_data.status
    order.total_cost = updated_data.total_cost

    # Optionally update items
    db.query(PurchaseOrderItem).filter(PurchaseOrderItem.purchase_order_id == order_id).delete()
    for item_data in updated_data.items:
        new_item = PurchaseOrderItem(
            purchase_order_id=order.id,
            supplier_product_id=item_data.supplier_product_id,
            quantity=item_data.quantity,
            unit_cost=item_data.unit_cost,
            subtotal=item_data.subtotal
        )
        db.add(new_item)

    db.commit()
    db.refresh(order)
    return order


# Delete Purchase Order
@purchase_order_router.delete("/{order_id}")
def delete_purchase_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Purchase Order not found")

    db.delete(order)
    db.commit()
    return {"detail": "Purchase Order and its items deleted successfully"}


# Get Purchase Order by Supplier ID
@purchase_order_router.get("/supplier/{supplier_id}", response_model=List[PurchaseOrderRead])
def get_orders_by_supplier(supplier_id: int, db: Session = Depends(get_db)):
    orders = db.query(PurchaseOrder).options(joinedload(PurchaseOrder.items)).filter(
        PurchaseOrder.supplier_id == supplier_id
    ).all()
    return orders


# Get Purchase Order by ID
@purchase_order_router.get("/{order_id}", response_model=PurchaseOrderRead)
def get_purchase_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(PurchaseOrder).options(joinedload(PurchaseOrder.items)).filter(
        PurchaseOrder.id == order_id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return order


# Update Purchase Order Status
@purchase_order_router.patch("/{order_id}/status", response_model=PurchaseOrderRead)
def update_purchase_order_status(order_id: int, status_update: PurchaseOrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Purchase Order not found")

    order.status = status_update.status
    db.commit()
    db.refresh(order)
    return order

