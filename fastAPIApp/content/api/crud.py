from sqlalchemy.orm import Session
from .. import models, schemas

class LocationDataManager:
    def __init__(self, db: Session):
        self.db = db

    def get_location_data(self, location_data_id: int):
        return self.db.query(models.LocationData).filter(models.LocationData.id == location_data_id).first()

    def get_locations_data_list(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.LocationData).offset(skip).limit(limit).all()

    def create_location_data(self, location_data: schemas.LocationDataCreate):
        new_location_data = models.LocationData(**location_data.dict())
        self.db.add(new_location_data)
        self.db.commit()
        self.db.refresh(new_location_data)
        return new_location_data

    def update_location_data(self, location_data_id: int, location_data: schemas.LocationDataCreate):
        existing_location_data = self.get_location_data(location_data_id)
        if existing_location_data:
            for var, value in vars(location_data).items():
                setattr(existing_location_data, var, value) if value else None
            self.db.commit()
            self.db.refresh(existing_location_data)
        return existing_location_data

    def delete_location_data(self, location_data_id: int):
        location_data_to_delete = self.get_location_data(location_data_id)
        if location_data_to_delete:
            self.db.delete(location_data_to_delete)
            self.db.commit()
            return True
        return False