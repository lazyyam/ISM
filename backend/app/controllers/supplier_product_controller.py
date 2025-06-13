from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.auth_dependencies import get_current_user
from app.database import get_db
from app.models.supplier_product_models import SupplierProduct
from app.schemas.supplier_product_schemas import SupplierProductCreate, SupplierProductUpdate, SupplierProductRead

supplier_product_router = APIRouter()


# Get All Supplier Products
@supplier_product_router.get("/", response_model=List[SupplierProductRead])
def get_supplier_products(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    products = db.query(SupplierProduct).filter(SupplierProduct.supplier_id == current_user.id).all()
    return products


# Add Supplier Product
@supplier_product_router.post("/", response_model=SupplierProductRead)
def create_supplier_product(
    product_data: SupplierProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing = db.query(SupplierProduct).filter(SupplierProduct.code == product_data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product code already exists.")

    new_product = SupplierProduct(
        **product_data.model_dump(),
        supplier_id=current_user.id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Edit/Update Supplier Product
@supplier_product_router.put("/{product_id}", response_model=SupplierProductRead)
def update_supplier_product(
    product_id: int,
    updated_data: SupplierProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    product = db.query(SupplierProduct).filter(
        SupplierProduct.id == product_id,
        SupplierProduct.supplier_id == current_user.id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


# Delete Supplier Product
@supplier_product_router.delete("/{product_id}")
def delete_supplier_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    product = db.query(SupplierProduct).filter(
        SupplierProduct.id == product_id,
        SupplierProduct.supplier_id == current_user.id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}


# Get Supplier Product by Supplier ID
@supplier_product_router.get("/by-supplier/{supplier_id}", response_model=List[SupplierProductRead])
def get_products_by_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    products = db.query(SupplierProduct).filter(SupplierProduct.supplier_id == supplier_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found for the given supplier ID")
    return products
