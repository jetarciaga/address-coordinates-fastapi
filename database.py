from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from fastapi import Depends
from typing import Annotated

#  Database connection details
engine = create_engine("sqlite:///./data.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(engine)
Base = declarative_base()


def get_db():
    """Opens connection to database and close it once session is done
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  Functions that interact with the database will rely to this.
DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


