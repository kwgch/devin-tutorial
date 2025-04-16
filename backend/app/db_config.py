import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

if os.getenv("FLY_APP_NAME"):
    DATABASE_URL = "sqlite:///:memory:"
    print("Using in-memory SQLite database for deployment")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/parallel_diary")
    print(f"Using database: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})

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
