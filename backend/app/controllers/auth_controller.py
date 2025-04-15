from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import jwt
from database import get_db
from models import User  
from schemas.user_schemas import UserCreate, UserLogin, ForgotPasswordRequest, ResetPasswordRequest
from fastapi.responses import JSONResponse
from utils.email import send_reset_email

SECRET_KEY = "ZM0xz9L7WB"  #random key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Generate JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@auth_router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)

    new_user = User(
        email=user.email, 
        password=hashed_password,
        full_name=user.full_name,
        role="supplier",
        phone_number=user.phone_number
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@auth_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token_payload = {
        "sub": db_user.email,
        "role": db_user.role,
        "email": db_user.email,  
        "id": str(db_user.id)    
    }
    
    token = create_access_token(
        token_payload, 
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": token, "token_type": "bearer"}
    



@auth_router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    reset_token = create_access_token({"sub": user.email}, timedelta(minutes=30))

    await send_reset_email(to_email=user.email, token=reset_token)

    return JSONResponse(content={
        "message": "Reset link sent to email",
    })


@auth_router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Reset link expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if verify_password(request.new_password, user.password):
        raise HTTPException(status_code=400, detail="New password cannot be the same as the old password")

    hashed_password = hash_password(request.new_password)
    user.password = hashed_password
    db.commit()

    return {"message": "Password reset successful"}
