from fastapi import FastAPI
from app.database import init_db, close_db
from app.api import routes
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(routes.router)