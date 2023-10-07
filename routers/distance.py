from database import DB_DEPENDENCY

from fastapi import APIRouter, HTTPException, Query
from starlette import status
from geopy.distance import geodesic

from models import Address

router = APIRouter()

@router.get("/distance", status_code=status.HTTP_200_OK)
async def get_address_area(db: DB_DEPENDENCY, 
                           latitude: float=Query(le=90, ge=-90), 
                           longitude: float=Query(le=180, ge=-180),
                           distance: float=Query(gt=0)):
    within_distance = []
    start_point = (latitude, longitude)
    addresses = db.query(Address).all()
    
    for address in addresses:
        address_point = (address.latitude, address.longitude)

        if geodesic(start_point, address_point).km <= float(distance):
            within_distance.append(address)
        
    if within_distance:
        return {"address": within_distance}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No saved address within area")
