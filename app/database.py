'''
Archivo que configura y abre las conexiones a MongoDB y MySQL,
y deja listas las sesiones para que el ETL pueda guardar y leer datos.
'''

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from pymongo import MongoClient

# Cargar .env
load_dotenv()

# ---------- SQLAlchemy Base ---------
class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

# ---------- MySQL ----------
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL, #type: ignore
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """FastAPI dependency for SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- MongoDB ----------
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_RAW_COLLECTION = os.getenv("MONGO_RAW_COLLECTION")

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB] #type: ignore
mongo_collection = mongo_db[MONGO_RAW_COLLECTION] #type: ignore