# Weather API Service

This project is a Weather API service built with **FastAPI**. It integrates with AWS DynamoDB and S3 for caching weather data and uses OpenWeatherMap for fetching live weather data. The service caches responses in DynamoDB and S3 for efficient querying and retrieval, with support for automatic expiration of cache entries.

---
## Project Features

- Fetch weather data from OpenWeatherMap by city name.
- Cache weather data in DynamoDB and S3 for 5 minutes.
- Dynamically create AWS resources during setup.
- Asynchronous API implementation for high performance.

---
## Setup Instructions

### Prerequisites

1. **AWS Permissions**:
   Ensure your [AWS](https://eu-north-1.signin.aws.amazon.com/) user has the necessary permissions for creating and interacting with:
   - **DynamoDB**
   - **S3**

  
   For larger projects, ask your DevOps team to configure these roles.


2. **Environment Variables**:
   Create a `.env` file from the `.env.template` file and populate the following variables:
   - AWS credentials and region:
     ```text
     AWS_ACCESS_KEY_ID=your_access_key
     AWS_SECRET_ACCESS_KEY=your_secret_key
     AWS_REGION_NAME=your_region
     ```
   - OpenWeatherMap API key:
     ```text
     OPENWEATHERMAP_API_KEY=your_api_key
     ```
   - Other project-specific configurations:
     ```text
     DYNAMODB_TABLE_NAME=your_dynamodb_table_name
     S3_BUCKET_NAME=your_s3_bucket_name
     ```

---

## Project Setup

#### 1. First-Time Setup with Service Initialization

Run the following command to build the Docker containers and initialize the DynamoDB table and S3 bucket:

```bash
SETUP_SERVICES=True docker-compose up --build
```

 > **_Note for Windows Users:_** If you are using Windows, run this command in Git Bash to 
ensure proper handling of environment variables.

#### 2. Regular Startup

After the initial setup, use the following command to start the project without rebuilding or recreating the AWS resources:

```bash
docker-compose up
```

If you need to rebuild the containers but skip AWS resource creation, use:

```bash
docker-compose up --build
```
---
## How to Access the OpenAPI Documentation

Once the server is running, you can access the interactive API documentation through FastAPI's built-in UI at the following URL:

- **[API Documentation (Swagger UI)](http://localhost:5000/docs#/)**

> **Note** If you changed yor local port, url can be different

---

## Code Formatting and Linting

This project uses **Black** for code formatting and **isort** for import sorting. Follow these steps to ensure your code adheres to the project's standards:

#### Using Black and isort

Use poetry shell to using black and isort
```bash
poetry shell
```

then you can use black .
```bash
black .
```
and isort
```bash
isort .
```

Or both tools together:
```bash
black . && isort .
```