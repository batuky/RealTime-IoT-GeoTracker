from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # Diğer cihaz özellikleri buraya eklenebilir.

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)
    # Diğer konum özellikleri buraya eklenebilir.

    device = relationship("Device")