from sqlalchemy.orm import Session
from . import models
from .schemas import DeviceCreate
from .exceptions import DeviceNotFoundError 

def create_device(db: Session, device: DeviceCreate) -> models.Device:
    """
    Create a new device and add it to the database.
    """
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_devices(db: Session, skip: int = 0, limit: int = 100) -> list[models.Device]:
    """
    Retrieve a list of devices from the database with optional pagination.
    """
    return db.query(models.Device).offset(skip).limit(limit).all()

def delete_device(db: Session, device_id: int) -> models.Device:
    """
    Delete a device from the database by its ID.
    If the device is not found, raise DeviceNotFoundError.
    """
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device is None:
        raise DeviceNotFoundError(device_id=device_id)
    db.delete(db_device)
    db.commit()
    return db_device

def get_device_by_id(db: Session, device_id: int) -> models.Device:
    """
    Retrieve a device by its ID from the database.
    If the device is not found, raise DeviceNotFoundError.
    """
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if db_device is None:
        raise DeviceNotFoundError(f"Device with id {device_id} not found.")
    return db_device

def get_locations_for_device(db: Session, device_id: int) -> list[models.Location]:
    """
    Retrieve all locations for a specified device by its ID.
    """
    device = get_device_by_id(db, device_id)
    return db.query(models.Location).filter(models.Location.device_id == device_id).all()