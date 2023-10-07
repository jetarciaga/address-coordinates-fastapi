from database import DB_DEPENDENCY

from models import Address, AddressBase
from starlette import status
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/address", status_code=status.HTTP_201_CREATED)
async def create_address(address: AddressBase, db: DB_DEPENDENCY):
    address = Address(**address.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.get("/address", status_code=status.HTTP_200_OK)
async def get_address(db: DB_DEPENDENCY):
    address = db.query(Address).all()
    return {"address": address}


@router.get("/address/{address_id}", status_code=status.HTTP_200_OK)
async def get_address_by_id(address_id, db: DB_DEPENDENCY):
    address = db.query(Address).get(address_id)
    return {"address": address}


@router.delete("/address/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id, db: DB_DEPENDENCY):
    address = db.query(Address).get(address_id)
    db.delete(address)
    db.commit()
    return {"address", address}


@router.put("/address/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_address(address_id, address_request: AddressBase, 
                          db: DB_DEPENDENCY):
    address = db.query(Address).get(address_id)
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="address not found.")
    elif address:
        address.latitude = address_request.latitude
        address.longitude = address_request.longitude
    else:
        address = Address(**address_request.model_dump())  # creates address if doesn't exist

    db.add(address)
    db.commit()
    db.refresh(address)

    return address   