import logging
from fastapi import FastAPI, Request
from .content.database import init_db, close_db
from .content.api import routes
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

# @app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body() 
    logger.info(f"Request: {body}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

app.include_router(routes.router)

logger.info("FastAPI app started.")