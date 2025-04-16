from typing import List, Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.models.diary import DiaryEntry, FavoriteExpression
from app.auth import UserCreate, get_password_hash, verify_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DatabaseService:
    """Service for database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            name=user_data.name,
            picture=user_data.picture
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def verify_user_password(self, email: str, password: str) -> Optional[User]:
        """Verify user credentials and return user if valid."""
        user = self.get_user_by_email(email)
        if user and verify_password(password, user.hashed_password):
            return user
        return None
    
    def create_diary_entry(self, user_id: str, content: str, translated_content: str) -> DiaryEntry:
        """Create a new diary entry."""
        db_entry = DiaryEntry(
            content=content,
            translated_content=translated_content,
            user_id=user_id
        )
        
        self.db.add(db_entry)
        self.db.commit()
        self.db.refresh(db_entry)
        
        return db_entry
    
    def get_diary_entry(self, entry_id: str) -> Optional[DiaryEntry]:
        """Get a diary entry by ID."""
        return self.db.query(DiaryEntry).filter(DiaryEntry.id == entry_id).first()
    
    def get_user_diary_entries(self, user_id: str) -> List[DiaryEntry]:
        """Get all diary entries for a user."""
        return self.db.query(DiaryEntry).filter(DiaryEntry.user_id == user_id).all()
    
    def update_diary_entry(self, entry_id: str, content: str, translated_content: str) -> Optional[DiaryEntry]:
        """Update a diary entry."""
        db_entry = self.get_diary_entry(entry_id)
        if not db_entry:
            return None
        
        db_entry.content = content
        db_entry.translated_content = translated_content
        
        self.db.commit()
        self.db.refresh(db_entry)
        
        return db_entry
    
    def delete_diary_entry(self, entry_id: str) -> bool:
        """Delete a diary entry."""
        db_entry = self.get_diary_entry(entry_id)
        if not db_entry:
            return False
        
        self.db.delete(db_entry)
        self.db.commit()
        
        return True
    
    def add_favorite_expression(self, entry_id: str, japanese_text: str, english_text: str, note: Optional[str] = None) -> Optional[FavoriteExpression]:
        """Add a favorite expression to a diary entry."""
        db_entry = self.get_diary_entry(entry_id)
        if not db_entry:
            return None
        
        db_expression = FavoriteExpression(
            japanese_text=japanese_text,
            english_text=english_text,
            note=note,
            diary_entry_id=entry_id
        )
        
        self.db.add(db_expression)
        self.db.commit()
        self.db.refresh(db_expression)
        
        return db_expression
    
    def get_user_favorite_expressions(self, user_id: str) -> List[FavoriteExpression]:
        """Get all favorite expressions for a user."""
        return (
            self.db.query(FavoriteExpression)
            .join(DiaryEntry)
            .filter(DiaryEntry.user_id == user_id)
            .all()
        )
