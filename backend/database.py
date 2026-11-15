import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


DEFAULT_DB = f"sqlite:///{Path(__file__).resolve().parent / 'astrovital.db'}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
pool_args = {"poolclass": StaticPool} if DATABASE_URL in {"sqlite://", "sqlite:///:memory:"} else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True, **pool_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
