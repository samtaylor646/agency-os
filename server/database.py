from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Use SQLite for development to ensure it works in Docker easily without a separate DB container.
# In production, this should be a PostgreSQL URL to support Row-Level Security if needed,
# but logical isolation is handled via `tenant_id` at the ORM level.

# Dynamically resolve an absolute path pointing to server/data/agency_os.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DEFAULT_DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'agency_os.db')}"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async Engine Setup
if DATABASE_URL.startswith("sqlite"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
    async_connect_args = {"check_same_thread": False}
    pool_args = {}
else:
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://") if DATABASE_URL.startswith("postgresql://") else DATABASE_URL
    async_connect_args = {}
    # Strict pool sizing and cost caps per Tech Design
    pool_args = {
        "pool_size": int(os.getenv("ASYNC_POOL_SIZE", 20)),
        "max_overflow": int(os.getenv("ASYNC_MAX_OVERFLOW", 10)),
        "pool_timeout": int(os.getenv("ASYNC_POOL_TIMEOUT", 10)),
    }

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    connect_args=async_connect_args,
    **pool_args
)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
