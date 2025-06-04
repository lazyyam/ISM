from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.sales_models import Sales
from models.product_models import Product
from models.product_batch_models import ProductBatch
from models.inventory_models import Inventory, TransactionTypeEnum
from schemas.sales_schemas import SaleCreate, SaleRead
from typing import List

sales_router = APIRouter()

# List all sales
@sales_router.get("/", response_model=List[SaleRead])
def get_sales(db: Session = Depends(get_db)):
    sales = db.query(Sales).all()
    result = []
    for sale in sales:
        result.append({
            "id": sale.id,
            "product_id": sale.product_id,
            "quantity": sale.quantity,
            "sell_date": sale.sell_date,
            "remarks": sale.remarks,
            "product_name": sale.product.name if sale.product else "Unknown"
        })
    return result

# Create a sale (FEFO: deduct from earliest expiry batches)
@sales_router.post("/", response_model=SaleRead)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # FEFO: Deduct from batches with earliest expiry
    batches = db.query(ProductBatch).filter(
        ProductBatch.product_id == sale.product_id,
        ProductBatch.quantity > 0
    ).order_by(ProductBatch.expiry_date.asc()).all()

    qty_to_sell = sale.quantity
    for batch in batches:
        if qty_to_sell <= 0:
            break
        deduct = min(batch.quantity, qty_to_sell)
        batch.quantity -= deduct
        qty_to_sell -= deduct

        # Record inventory
        inventory_entry = Inventory(
            product_id=sale.product_id,
            change_amount=-deduct,
            transaction_type=TransactionTypeEnum.sale,
            batch_id=batch.batch_id
        )
        db.add(inventory_entry)

    if qty_to_sell > 0:
        raise HTTPException(status_code=400, detail="Not enough stock to complete sale")

    new_sale = Sales(
        product_id=sale.product_id,
        quantity=sale.quantity,
        sell_date=sale.sell_date,
        remarks=sale.remarks
    )
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return {
        "id": new_sale.id,
        "product_id": new_sale.product_id,
        "quantity": new_sale.quantity,
        "sell_date": new_sale.sell_date,
        "remarks": new_sale.remarks,
        "product_name": product.name if product else "Unknown"
    }