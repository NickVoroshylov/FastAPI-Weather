import json
import logging

import aioboto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

from app.core.config import AWS_REGION_NAME, S3_BUCKET_NAME

logger = logging.getLogger(__name__)


async def insert_weather_file_s3(city: str, timestamp: str, data: dict) -> str:
    """
    Uploads a weather data file to S3 and returns the S3 object URL.
    """
    file_name = f"{city}_{timestamp}.json"
    session = aioboto3.Session()

    try:
        async with session.client("s3", region_name=AWS_REGION_NAME) as s3_client:
            await s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=file_name, Body=str(data))
            s3_url = f"s3://{S3_BUCKET_NAME}/{file_name}"

            logger.info(f"Weather data saved to S3 for city: {city}. S3 URL: {s3_url}")
            return s3_url

    except ClientError as e:
        logger.error(f"Failed to upload weather file to S3. City: {city}, Timestamp: {timestamp}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload data to S3")

    except Exception as e:
        logger.exception(
            f"Unexpected error occurred while uploading weather file to S3. City: {city}, Timestamp: {timestamp}"
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_cached_response_from_s3(s3_url: str) -> dict:
    """
    Retrieves a JSON response from S3 based on the provided S3 URL.
    """

    try:
        if not s3_url.startswith("s3://"):
            raise ValueError("Invalid S3 URL. Ensure it starts with 's3://'.")

        url_parts = s3_url.replace("s3://", "").split("/", 1)
        if len(url_parts) != 2:
            raise ValueError("Invalid S3 URL format. Expected format: 's3://bucket/key'.")

        bucket_name, key = url_parts
        logger.info(f"Downloading cached response from bucket '{bucket_name}' and key '{key}'.")

        session = aioboto3.Session()
        async with session.client("s3", region_name=AWS_REGION_NAME) as s3_client:
            response = await s3_client.get_object(Bucket=bucket_name, Key=key)
            content = await response["Body"].read()

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                decoded_content = content.decode("utf-8").replace("'", '"')
                return json.loads(decoded_content)

    except ClientError as e:
        logger.error(f"Error accessing S3: {e}")
        raise ValueError("Failed to retrieve the cached from S3.")

    except Exception as e:
        logger.exception(f"Unexpected error while fetching cached response: {e}")
        raise ValueError("An unexpected error occurred while retrieving the cached response.")
