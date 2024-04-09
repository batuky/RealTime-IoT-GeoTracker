from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app import schemas
from app.crud import create_device, get_devices, delete_device
from app import models

router = APIRouter(prefix="/devices", tags=["devices"])

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Device)
async def create_device_endpoint(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """
    Create a new device in the database.
    """
    return create_device(db=db, device=device)

@router.get("/", response_model=List[schemas.Device])
async def list_devices_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List devices from the database with optional pagination.
    """
    return get_devices(db, skip=skip, limit=limit)

@router.delete("/{device_id}", response_model=schemas.Device)
async def delete_device_endpoint(device_id: int = Path(..., description="The ID of the device to delete"), db: Session = Depends(get_db)):
    """
    Delete a device from the database by ID.
    """
    db_device = delete_device(db=db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device