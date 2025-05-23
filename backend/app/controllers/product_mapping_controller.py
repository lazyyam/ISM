from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.product_mapping_models import ProductMapping
from schemas.product_mapping_schemas import ProductMappingCreate, ProductMappingRead

product_mapping_router = APIRouter()

# Get all mappings
@product_mapping_router.get("/", response_model=List[ProductMappingRead])
def get_all_mappings(db: Session = Depends(get_db)):
    return db.query(ProductMapping).all()

# Create or update a mapping
@product_mapping_router.post("/", response_model=ProductMappingRead)
def create_or_update_mapping(
    mapping: ProductMappingCreate,
    db: Session = Depends(get_db)
):
    # Check if mapping exists
    existing = db.query(ProductMapping).filter(
        ProductMapping.supplier_product_id == mapping.supplier_product_id
    ).first()
    if existing:
        existing.product_id = mapping.product_id
        db.commit()
        db.refresh(existing)
        return existing
    new_mapping = ProductMapping(
        supplier_id=mapping.supplier_id,
        supplier_product_id=mapping.supplier_product_id,
        product_id=mapping.product_id
    )
    db.add(new_mapping)
    db.commit()
    db.refresh(new_mapping)
    return new_mapping

# Delete a mapping
@product_mapping_router.delete("/{mapping_id}")
def delete_mapping(mapping_id: int, db: Session = Depends(get_db)):
    mapping = db.query(ProductMapping).filter(ProductMapping.id == mapping_id).first()
    if not mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    db.delete(mapping)
    db.commit()
    return {"detail": "Mapping deleted"}