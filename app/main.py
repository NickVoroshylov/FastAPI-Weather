from fastapi import FastAPI

from app.api.router import router as weather_router
from app.core.config import SETUP_SERVICES
from app.core.logging_config import setup_logging
from app.utils.setup_services import setup_resources

setup_logging()

app = FastAPI(title="FastAPI Weather App")

app.include_router(weather_router)


@app.on_event("startup")
async def on_startup():
    """FastAPI startup event."""

    if SETUP_SERVICES:
        await setup_resources()
