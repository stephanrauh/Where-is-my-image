from sqlalchemy import Column, Integer, String, DateTime, Float, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    filepath = Column(String)
    file_size = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    format = Column(String)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)
    exif_data = Column(Text)
    tags = Column(Text)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://photo_user:photo_pass@localhost:5432/photo_browser")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    import time
    max_retries = 5
    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("Database tables created successfully!")
            return
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying in 3 seconds...")
                time.sleep(3)
            else:
                print("Failed to create database tables after all retries")
                raise