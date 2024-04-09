from fastapi import FastAPI
from app.database import init_db, close_db
from app.routers import device, location

app = FastAPI()

app.include_router(device.router)
app.include_router(location.router)

@app.router.on_event("startup")
async def startup_event():
    init_db()

@app.router.on_event("shutdown")
async def shutdown_event():
    close_db()