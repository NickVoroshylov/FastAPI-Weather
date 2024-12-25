import logging
from datetime import datetime, timedelta

import aioboto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

from app.core.config import AWS_REGION_NAME, CACHE_MINUTES, DYNAMODB_TABLE_NAME

logger = logging.getLogger("app")


async def insert_weather_data_dynamodb(city: str, timestamp: str, s3_url: str):
    """
    Uploads a response weather metadata into a DynamoDB table.
    """
    session = aioboto3.Session()

    try:
        async with session.client("dynamodb", region_name=AWS_REGION_NAME) as dynamodb_client:
            await dynamodb_client.put_item(
                TableName=DYNAMODB_TABLE_NAME,
                Item={
                    "city": {"S": city},
                    "timestamp": {"S": timestamp},
                    "s3_url": {"S": s3_url},
                },
            )
            logger.info(f"Weather metadata saved to DynamoDB for city: {city} at {timestamp} with S3 URL: {s3_url}")

    except ClientError as e:
        logger.error(
            f"Failed to insert weather data into DynamoDB. City: {city}, Timestamp: {timestamp}, Error: {str(e)}"
        )
        raise HTTPException(status_code=500, detail="Failed to insert data into DynamoDB")

    except Exception as e:
        logger.exception(
            f"Unexpected error occurred during inserting data into DynamoDB. City: {city}, Timestamp: {timestamp}"
        )
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_last_cached_record_by_city(city: str):
    """
    Return last item by timestamp for passed city.
    """
    session = aioboto3.Session()

    try:
        async with session.client("dynamodb", region_name=AWS_REGION_NAME) as dynamodb_client:
            response = await dynamodb_client.query(
                TableName=DYNAMODB_TABLE_NAME,
                KeyConditionExpression="city = :city",
                ExpressionAttributeValues={":city": {"S": city}},
                ScanIndexForward=False,
                Limit=1,
            )

            if not response.get("Items"):
                logger.info(f"No records found for city: {city}")
                return None

            item = response["Items"][0]
            timestamp = item["timestamp"]["S"]
            cache_time = datetime.fromisoformat(timestamp)

            if datetime.utcnow() - cache_time < timedelta(minutes=CACHE_MINUTES):
                logger.info(f"Cache is valid for city: {city}")
                return item["s3_url"]["S"]

            logger.info(f"Cache expired for city: {city}")
            return None

    except Exception as e:
        logger.error(f"Error fetching cache for city: {city}: {e}")
