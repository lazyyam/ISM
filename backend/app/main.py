from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, Base, engine
from controllers.auth_controller import auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    result = db.execute(text("SHOW TABLES;")).fetchall()
    tables = [row[0] for row in result] 
    return {"tables": tables}

@app.get("/")
async def root():
    return {"message": "FastAPI is running"}