from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db, Base, engine
from app.controllers.auth_controller import auth_router
from app.controllers.product_controller import product_router
from app.controllers.supplier_controller import supplier_router
from app.controllers.supplier_product_controller import supplier_product_router
from app.controllers.purchase_order_controller import purchase_order_router
from app.controllers.product_mapping_controller import product_mapping_router
from app.controllers.sales_controller import sales_router
from app.controllers.supplier_bank_account_controller import supplier_bank_account_router
from app.controllers.inventory_controller import inventory_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ism-vuejs-production.up.railway.app"],  # deployed frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# local dev frontend http://localhost:8080
# prod frontend https://ism-vuejs-production.up.railway.app

Base.metadata.create_all(bind=engine)

os.makedirs("/data/uploads", exist_ok=True)

#app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")
app.mount("/uploads", StaticFiles(directory="/data/uploads"), name="uploads")


app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(product_router, prefix="/api/products", tags=["Products"])
app.include_router(supplier_router, prefix="/api/suppliers", tags=["Suppliers"])
app.include_router(supplier_product_router, prefix="/api/supplier-products", tags=["Supplier Products"])
app.include_router(purchase_order_router, prefix="/api/purchase-orders", tags=["Purchase Orders"])
app.include_router(product_mapping_router, prefix="/api/product-mappings", tags=["Product Mappings"])
app.include_router(sales_router, prefix="/api/sales", tags=["Sales"])
app.include_router(supplier_bank_account_router, prefix="/api/supplier-bank-accounts", tags=["Supplier Bank Accounts"])
app.include_router(inventory_router, prefix="/api/inventory", tags=["Inventory"])

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SHOW TABLES;")).fetchall()
    tables = [row[0] for row in result] 
    return {"tables": tables}

@app.get("/")
async def root():
    return {"message": "FastAPI is running"}

