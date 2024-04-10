from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas 
from ..database import SessionLocal  # Veritabanı bağlantı fonksiyonunu içe aktar

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/iot_data/", response_model=schemas.Location)
def create_iot_data(location_create: schemas.LocationCreate, db: Session = Depends(get_db)):
    db_location = models.Location(**location_create.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.get("/iot_data/", response_model=List[schemas.Location])
def read_all_iot_data(db: Session = Depends(get_db)):
    locations = db.query(models.Location).all()
    return locations

@router.get("/iot_data/{iot_data_id}", response_model=schemas.Location)
def read_iot_data(iot_data_id: int, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == iot_data_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@router.delete("/iot_data/{iot_data_id}", response_model=schemas.Location)
def delete_iot_data(iot_data_id: int, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == iot_data_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_location)
    db.commit()
    return db_location

@router.get("/iot_location_history/{device_id}", response_model=List[schemas.Location])
def read_device_location_history(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device.locations