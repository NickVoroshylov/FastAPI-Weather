import logging

import aioboto3

from app.core.config import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION_NAME,
    AWS_SECRET_ACCESS_KEY,
    DYNAMODB_TABLE_NAME,
    S3_BUCKET_NAME,
)

logger = logging.getLogger(__name__)


async def create_s3_bucket():
    """Creates a S3 bucket async"""
    session = aioboto3.Session()

    async with session.client("s3", region_name=AWS_REGION_NAME) as s3_client:
        try:
            # Check if bucket exists by listing all buckets and comparing names
            response = await s3_client.list_buckets()
            bucket_names = [bucket["Name"] for bucket in response["Buckets"]]

            if S3_BUCKET_NAME in bucket_names:
                logger.info(f"S3 bucket '{S3_BUCKET_NAME}' already exists.")
                return

            # Create the bucket if it doesn't exist
            await s3_client.create_bucket(
                Bucket=S3_BUCKET_NAME, CreateBucketConfiguration={"LocationConstraint": AWS_REGION_NAME}
            )
            logger.info(f"S3 bucket '{S3_BUCKET_NAME}' created successfully.")
        except Exception as e:
            logger.error(f"Error checking or creating S3 bucket: {e}")
            raise


async def create_dynamodb_table():
    """Creates a DynamoDB table async."""
    session = aioboto3.Session()

    async with session.client("dynamodb", region_name=AWS_REGION_NAME) as dynamodb_client:
        try:
            response = await dynamodb_client.list_tables()
            if DYNAMODB_TABLE_NAME in response["TableNames"]:
                logger.info(f"DynamoDB table '{DYNAMODB_TABLE_NAME}' already exists.")
                return

            await dynamodb_client.create_table(
                TableName=DYNAMODB_TABLE_NAME,
                KeySchema=[
                    {"AttributeName": "city", "KeyType": "HASH"},  # Partition key
                    {"AttributeName": "timestamp", "KeyType": "RANGE"},  # Sort key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "city", "AttributeType": "S"},
                    {"AttributeName": "timestamp", "AttributeType": "S"},
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            logger.info(f"DynamoDB table '{DYNAMODB_TABLE_NAME}' created successfully.")
        except Exception as e:
            logger.error(f"Error creating DynamoDB table: {e}")
            raise


async def setup_resources():
    """Setup AWS resources on app startup."""
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        logger.warning("AWS credentials are not provided. Skipping resource creation.")
        return

    logger.info("Starting AWS resource setup.")
    await create_s3_bucket()
    await create_dynamodb_table()
    logger.info("AWS resource setup completed.")
