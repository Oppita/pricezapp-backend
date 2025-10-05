from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔧 Reemplaza SOLO [YOUR-PASSWORD] por tu contraseña real (sin corchetes)
DATABASE_URL = "postgresql://postgres.kxxqwldqdljfpcucntdg:Virumafia123%2A@aws-1-sa-east-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
