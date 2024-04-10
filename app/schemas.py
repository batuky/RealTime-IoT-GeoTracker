from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Device modeli için Pydantic schema
class DeviceBase(BaseModel):
    name: str

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    locations: List['Location'] = []

    class Config:
        from_attributes = True

# Location modeli için Pydantic schema
class LocationBase(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime

class LocationCreate(LocationBase):
    device_id: int

class Location(LocationBase):
    id: int
    device_id: int

    class Config:
        from_attributes = True

# Pydantic modellerinde forward declaration kullanımı
Device.model_rebuild()