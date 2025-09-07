"""Database setup and session management for Outreach AI."""
import os
from .models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Determine database URL from environment variable, defaulting to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./outreach.db")

# Additional connect args for SQLite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """Provide a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database by creating all tables."""
    Base.metadata.create_all(bind=engine)
