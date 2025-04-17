import os
import sys
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

is_fly_deployment = os.getenv("FLY_APP_NAME") is not None

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    if is_fly_deployment:
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@parallel-diary-db.internal:5432/parallel_diary")
        print(f"Using PostgreSQL for Fly.io deployment: {DATABASE_URL}", file=sys.stderr)
    else:
        DATABASE_URL = "postgresql://postgres:postgres@localhost/parallel_diary"
        print(f"Using local database: {DATABASE_URL}", file=sys.stderr)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting a database session.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
