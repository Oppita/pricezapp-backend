# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Leer URL desde variable de entorno (configurar en Render)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")  # fallback local sqlite

# Si se usa postgres, create_engine detectará el driver
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
