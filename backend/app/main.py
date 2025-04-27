from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, Base, engine
from controllers.auth_controller import auth_router
from controllers.product_controller import product_router
from controllers.supplier_controller import supplier_router
from controllers.supplier_product_controller import supplier_product_router
from controllers.purchase_order_controller import purchase_order_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(product_router, prefix="/api/products", tags=["Products"])
app.include_router(supplier_router, prefix="/api/suppliers", tags=["Suppliers"])
app.include_router(supplier_product_router, prefix="/api/supplier-products", tags=["Supplier Products"])
app.include_router(purchase_order_router, prefix="/api/purchase-orders", tags=["Purchase Orders"])


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SHOW TABLES;")).fetchall()
    tables = [row[0] for row in result] 
    return {"tables": tables}

@app.get("/")
async def root():
    return {"message": "FastAPI is running"}