import logging
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas 
from ..database import SessionLocal


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.info")

router = APIRouter()

def get_db():
    
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print(e)
    else:
        print("success")    
    finally:
        db.close()
        logger.info("Database connection closed")


@router.post("/iot_data/", response_model=schemas.Location)
def create_iot_data(location_create:schemas.LocationCreate, db: Session = Depends(get_db)):
    # Extract the nested 'location' data
    location_data = location_create.dict(by_alias=True)
    nested_location = location_data.pop('location', {})  # Remove 'location' and get its value
    print(location_data)
    # Merge the nested 'location' data with the top-level data
    flat_data = {**location_data, **nested_location}

    # Now flat_data has a flat structure suitable for models.Location
    db_location = models.Location(**flat_data)
    print(db_location)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    logger.info(f"New IoT data created with ID: {db_location.id}")
    location_response = {
        'id': db_location.id,
        'device_id': db_location.device_id,
        # 'timestamp' field is expected, and it corresponds to the 'time' field in the ORM model
        'time': db_location.time,
        # The 'location' is directly taken from the nested LocationData instance
        'location': {
            'latitude': db_location.latitude,
            'longitude': db_location.longitude,
        },
        # The 'time' field is not necessary here as it is an alias for 'timestamp' in the LocationBase schema
    }
    return schemas.LocationCreate(**location_response)



@router.get("/iot_data/", response_model=List[schemas.Location])
def read_all_iot_data(db: Session = Depends(get_db)):
    locations = db.query(models.Location).all()
    logger.info("All IoT data read")
    return locations

@router.get("/iot_data/{iot_data_id}", response_model=schemas.Location)
def read_iot_data(iot_data_id: int, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == iot_data_id).first()
    if db_location is None:
        logger.warning(f"Location with ID {iot_data_id} not found")
        raise HTTPException(status_code=404, detail="Location not found")
    logger.info(f"Data for location ID {iot_data_id} retrieved")
    return db_location

@router.delete("/iot_data/{iot_data_id}", response_model=schemas.Location)
def delete_iot_data(iot_data_id: int, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == iot_data_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_location)
    db.commit()
    logger.info(f"Location with ID {iot_data_id} deleted")
    return db_location

@router.get("/iot_location_history/{device_id}", response_model=List[schemas.Location])
def read_device_location_history(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device is None:
        logger.warning(f"Device with ID {device_id} not found")
        raise HTTPException(status_code=404, detail="Device not found")
    logger.info(f"Location history for device ID {device_id} retrieved")
    return db_device.locations