from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from models import UserCreate, UserLogin, TokenResponse
from database import get_db, engine, Base, User
from auth_utils import (
    create_access_token, 
    verify_token, 
    get_password_hash, 
    verify_password,
    get_google_user_info
)

load_dotenv()

app = FastAPI(title="Authentication Microservice", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.post("/auth/signup", response_model=TokenResponse)
async def signup(user_data: UserCreate, db=Depends(get_db)):
    """Sign up with email and password"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email
    )

@app.post("/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db=Depends(get_db)):
    """Login with email and password"""
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email
    )

@app.get("/auth/google")
async def google_login():
    """Initiate Google OAuth2 login"""
    google_client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")
    
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": google_client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline"
    }
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return {"auth_url": f"{auth_url}?{query_string}"}

@app.get("/auth/google/callback", response_model=TokenResponse)
async def google_callback(code: str, db=Depends(get_db)):
    """Handle Google OAuth2 callback"""
    try:
        user_info = await get_google_user_info(code)
        
        # Check if user exists
        user = db.query(User).filter(User.email == user_info["email"]).first()
        
        if not user:
            # Create new user
            user = User(
                email=user_info["email"],
                full_name=user_info.get("name", ""),
                google_id=user_info.get("sub")
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google authentication failed: {str(e)}"
        )

@app.get("/auth/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    """Get current user information (protected endpoint)"""
    try:
        payload = verify_token(credentials.credentials)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active
    }

@app.get("/auth/verify")
async def verify_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify access token (protected endpoint)"""
    try:
        payload = verify_token(credentials.credentials)
        return {"valid": True, "user_email": payload.get("sub")}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 