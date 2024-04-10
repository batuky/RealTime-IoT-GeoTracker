from sqlalchemy.orm import Session
from .. import models, schemas

def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(name=device.name)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()

def get_all_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Device).offset(skip).limit(limit).all()

def delete_device(db: Session, device_id: int):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device is not None:
        db.delete(db_device)
        db.commit()
        return True
    return False

def get_latest_location_for_device(db: Session, device_id: int):
    return db.query(models.Location).filter(models.Location.device_id == device_id).order_by(models.Location.timestamp.desc()).first()

# def get_latest_location_for_all_devices(db: Session):
#     devices = get_all_devices(db)
#     latest_locations = []
#     for device in devices:
#         latest_location = get_latest_location_for_device(db, device.id)
#         if latest_location:
#             latest_locations.append(latest_location)
#     return latest_locations