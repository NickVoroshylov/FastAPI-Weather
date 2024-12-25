import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from starlette.responses import JSONResponse

from app.services.dynamodb import get_last_cached_record_by_city, insert_weather_data_dynamodb
from app.services.openweather import fetch_weather_by_city
from app.services.s3_bucket import get_cached_response_from_s3, insert_weather_file_s3

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/weather")
async def get_weather(city: str = Query(...)):
    """
    Fetches weather data for the specified city, uploads response as .json to S3, and metadata to DynamoDB.
    """
    try:
        # Check cache
        cached_data_url = await get_last_cached_record_by_city(city)
        if cached_data_url:
            cached_response = await get_cached_response_from_s3(cached_data_url)
            return {"message": "Cache hit", "weather_data": cached_response, "s3_url": cached_data_url}

        # Fetch weather data
        response = await fetch_weather_by_city(city)
        if not response:
            logger.warning(f"Weather data for city '{city}' could not be fetched.")
            raise HTTPException(status_code=404, detail=f"Weather data for city '{city}' not found or unavailable.")

        timestamp = datetime.utcnow().isoformat()

        # save response as .json file into S3 bucket
        s3_url = await insert_weather_file_s3(city, timestamp, response)

        # save metadata into DynamoDB table
        await insert_weather_data_dynamodb(city, timestamp, s3_url)

        return {"weather_data": response, "s3_url": s3_url}

    except HTTPException as http_exc:
        logger.error(f"HTTP error while processing city {city}: {http_exc.detail}")
        return JSONResponse(
            status_code=http_exc.status_code,
            content={"detail": http_exc.detail},
        )

    except Exception as exc:
        logger.exception(f"Unexpected error occurred while processing city: {city}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later.",
        )
