from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

from app.auth import User, UserCreate, create_access_token, Token, get_current_user
from app.database import db

router = APIRouter(prefix="/auth", tags=["authentication"])

import os
from dotenv import load_dotenv

load_dotenv()

config = Config(environ={
    "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID"),
    "GOOGLE_CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET")
})

oauth = OAuth(config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/login")
async def login(request: Request):
    """Redirect to Google OAuth login."""
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request):
    """Handle OAuth callback from Google."""
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    
    email = user_info.get("email")
    user = db.get_user_by_email(email)
    
    if not user:
        user_data = UserCreate(
            email=email,
            name=user_info.get("name"),
            picture=user_info.get("picture")
        )
        user = db.create_user(user_data)
    
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email}
    )
    
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173/auth-callback")
    return RedirectResponse(
        url=f"{frontend_url}?token={access_token}",
        status_code=status.HTTP_303_SEE_OTHER
    )

@router.get("/me", response_model=User)
async def get_current_user(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user."""
    return current_user
