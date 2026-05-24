from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Use SQLite for development to ensure it works in Docker easily without a separate DB container.
# In production, this should be a PostgreSQL URL to support Row-Level Security if needed,
# but logical isolation is handled via `tenant_id` at the ORM level.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agency_os.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
