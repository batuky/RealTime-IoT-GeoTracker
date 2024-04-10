from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DeviceBase(BaseModel):
    name: str

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    locations: List['Location'] = []

    class Config:
        orm_mode = True

class LocationData(BaseModel):
    latitude: float
    longitude: float

# class LocationBase(BaseModel):
#     timestamp: datetime = Field(..., alias='time')
#     location: LocationData

class LocationBase(BaseModel):
    timestamp: datetime = Field(..., alias='time')
    location: Optional[LocationData] = None

class LocationCreate(LocationBase):
    device_id: int
    # This class Config is necessary for Pydantic to handle the alias 'time'
    class Config:
        allow_population_by_field_name = True

class Location(LocationBase):
    id: int
    location: LocationData
    time: datetime
    device_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

Device.update_forward_refs()