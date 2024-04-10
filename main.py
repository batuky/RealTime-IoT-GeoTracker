import logging
from fastapi import FastAPI
from app.database import init_db, close_db
from app.api import routes
from contextlib import asynccontextmanager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application is starting...")
    init_db()
    yield
    close_db()
    logger.info("Application is closing...")

app = FastAPI(lifespan=lifespan)

app.include_router(routes.router)

logger.info("FastAPI app started.")