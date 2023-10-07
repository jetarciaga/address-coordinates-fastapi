from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from database import SessionLocal, Base, engine
from models import Address, AddressBase
from starlette import status


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
Base.metadata.create_all(bind=engine)  # initialize database
DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


@app.post("/address", status_code=status.HTTP_201_CREATED)
async def create_location(location: AddressBase, db: DB_DEPENDENCY):
    location = Address(**location.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@app.get("/address", status_code=status.HTTP_200_OK)
async def get_location(db: DB_DEPENDENCY):
    locations = db.query(Address).all()
    return {"locations": locations}


@app.get("/address/{address_id}", status_code=status.HTTP_200_OK)
async def get_location_by_id(address_id, db: DB_DEPENDENCY):
    location = db.query(Address).get(address_id)
    return {"location": location}


@app.delete("/address/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(address_id, db: DB_DEPENDENCY):
    location = db.query(Address).get(address_id)
    return {"location", location}


@app.put("/address/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_location(address_id, location_request: AddressBase, 
                          db: DB_DEPENDENCY):
    location = db.query(Address).get(address_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Location not found.")
    elif location:
        location.latitude = location_request.latitude
        location.longitude = location_request.longitude
    else:
        location = Address(**location_request.model_dump())  # creates location if doesn't exist

    db.add(location)
    db.commit()
    db.refresh(location)

    return location    
    