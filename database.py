from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from fastapi import Depends
from typing import Annotated


engine = create_engine("sqlite:///./data.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


