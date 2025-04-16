from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

from app.auth import User, UserCreate, create_access_token, Token, get_current_user
from app.database import db

router = APIRouter(tags=["authentication"])

import os
from dotenv import load_dotenv

load_dotenv()

class UserRegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register", response_model=Token)
async def register(user_data: UserRegisterRequest):
    """新規ユーザー登録エンドポイント"""
    existing_user = db.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="このメールアドレスは既に登録されています。"
        )
    
    user = db.create_user(UserCreate(
        email=user_data.email,
        password=user_data.password,
        name=user_data.name
    ))
    
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user_data: UserLoginRequest):
    """ユーザーログインエンドポイント"""
    user = db.verify_user_password(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません。",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "name": user.name}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def get_current_user(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user."""
    return current_user
