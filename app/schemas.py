from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Cihaz Schemaları
class DeviceBase(BaseModel):
    name: str

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int

    class Config:
        orm_mode = True

# Konum Schemaları
class LocationBase(BaseModel):
    latitude: float
    longitude: float
    timestamp: Optional[datetime] = None

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    device_id: int

    class Config:
        orm_mode = True