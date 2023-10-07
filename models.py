from typing import Optional
from database import Base
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DECIMAL


class Address(Base):
    __tablename__ = "coordinates"

    id = Column(Integer, primary_key=True)
    latitude = Column(DECIMAL)
    longitude = Column(DECIMAL)
    description = Column(String(255), nullable=True)


class AddressBase(BaseModel):
    latitude: float
    longitude: float
    description: Optional[str] = Field(None)