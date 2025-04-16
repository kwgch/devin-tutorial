from sqlalchemy import create_engine
from app.db_config import Base, engine
from app.models.user import User
from app.models.diary import DiaryEntry, FavoriteExpression

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
