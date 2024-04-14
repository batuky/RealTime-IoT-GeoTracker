from datetime import datetime

from pydantic import BaseModel, Field


class LocationDataBase(BaseModel):
    device: int = Field(..., description="The ID of the device")
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")
 
class LocationDataCreate(LocationDataBase):
    time: datetime = Field(None, description="Time when the location data was recorded")

class LocationDataRead(LocationDataBase):
    id: int = Field(..., description="Unique ID of the location data")
    time: datetime = Field(..., description="Time when the location data was recorded")

    class Config:
        orm_mode = True