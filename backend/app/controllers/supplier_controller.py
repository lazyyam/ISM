from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_models import User  
from app.schemas.user_schemas import UserResponse

supplier_router = APIRouter()

@supplier_router.get("/", response_model=List[UserResponse])
def get_all_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(User).filter(User.role == "supplier").all()
    return suppliers
