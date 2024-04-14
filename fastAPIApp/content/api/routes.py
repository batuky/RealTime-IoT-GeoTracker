from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import database, schemas
from .crud import LocationDataManager

router = APIRouter()

class LocationDataController:
    def __init__(self, db: Session):
        self.manager = LocationDataManager(db)

    def read_location_data(self, location_data_id: int):
        location_data = self.manager.get_location_data(location_data_id)
        if location_data is None:
            raise HTTPException(status_code=404, detail="Location data not found")
        return location_data

    def read_location_datas(self, skip: int = 0, limit: int = 100):
        return self.manager.get_locations_data_list(skip=skip, limit=limit)

    def create_location_data(self, location_data: schemas.LocationDataCreate):
        return self.manager.create_location_data(location_data)

    def update_location_data(self, location_data_id: int, location_data: schemas.LocationDataCreate):
        updated_data = self.manager.update_location_data(location_data_id, location_data)
        if updated_data is None:
            raise HTTPException(status_code=404, detail="Location data not found")
        return updated_data

    def delete_location_data(self, location_data_id: int):
        if not self.manager.delete_location_data(location_data_id):
            raise HTTPException(status_code=404, detail="Location data not found")
        return {"ok": True}

@router.get("/locations-data/{location_data_id}", response_model=schemas.LocationDataRead)
def read_location_data(location_data_id: int, db: Session = Depends(database.get_db)):
    controller = LocationDataController(db)
    return controller.read_location_data(location_data_id)

@router.get("/locations-data/", response_model=list[schemas.LocationDataRead])
def read_location_datas(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    controller = LocationDataController(db)
    return controller.read_location_datas(skip=skip, limit=limit)

@router.post("/locations-data/", response_model=schemas.LocationDataRead)
def create_location_data(location_data: schemas.LocationDataCreate, db: Session = Depends(database.get_db)):
    controller = LocationDataController(db)
    return controller.create_location_data(location_data)

@router.put("/locations-data/{location_data_id}", response_model=schemas.LocationDataRead)
def update_location_data(location_data_id: int, location_data: schemas.LocationDataCreate, db: Session = Depends(database.get_db)):
    controller = LocationDataController(db)
    return controller.update_location_data(location_data_id, location_data)

@router.delete("/locations-data/{location_data_id}", status_code=204)
def delete_location_data(location_data_id: int, db: Session = Depends(database.get_db)):
    controller = LocationDataController(db)
    return controller.delete_location_data(location_data_id)