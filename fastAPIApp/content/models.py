from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LocationData(Base):
    __tablename__ = "location_data"

    id = Column(Integer, primary_key=True, index=True)
    device = Column(Integer, nullable=False)
    time = Column(DateTime, default=datetime.now)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)