import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api import router
from app.auth_routes import router as auth_router
from app.db_init import init_db

app = FastAPI(title="Parallel Diary API", description="API for Japanese-English diary application")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

app.include_router(router, prefix="/api")
app.include_router(auth_router, prefix="/auth")

@app.on_event("startup")
async def startup_event():
    init_db()
    print("Database initialized successfully.")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
