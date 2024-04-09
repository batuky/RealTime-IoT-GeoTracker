from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app import exceptions, models
from app.crud import get_locations_for_device
from app import schemas  # Assuming that this function is implemented in the crud module

router = APIRouter(prefix="/locations", tags=["locations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{device_id}", response_model=List[schemas.Location])
async def get_locations_by_device_endpoint(device_id: int = Path(..., description="The ID of the device to retrieve locations for"), db: Session = Depends(get_db)):
    """
    Retrieve all locations for a specified device by its ID.
    """
    try:
        locations = get_locations_for_device(db, device_id=device_id)
    except exceptions.DeviceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving locations.")

    if not locations:
        raise HTTPException(status_code=404, detail="No locations found for this device")
    
    return locations