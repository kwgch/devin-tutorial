from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from pydantic import BaseModel

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Must be set in environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="auth/login",
    tokenUrl="auth/token",
)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    sub: Optional[str] = None

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Validate the token and return the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        sub: str = payload.get("sub")
        
        if email is None or sub is None:
            raise credentials_exception
        
        token_data = TokenData(email=email, sub=sub)
    except JWTError:
        raise credentials_exception
    
    from app.database import get_user_by_email
    user = get_user_by_email(email)
    
    if user is None:
        raise credentials_exception
    
    return user
