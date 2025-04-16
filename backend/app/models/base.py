from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.db_config import Base

def generate_uuid():
    """Generate a UUID string."""
    return str(uuid4())
