# app/data/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://user:password@db:5432/dbname"  # fallback if env var is missing
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
