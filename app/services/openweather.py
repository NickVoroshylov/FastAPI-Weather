import logging

import aiohttp

from app.core.config import OPENWEATHERMAP_API_KEY, OPENWEATHERMAP_BASE_URL

logger = logging.getLogger(__name__)


async def fetch_weather_by_city(city: str):
    url = f"{OPENWEATHERMAP_BASE_URL}?q={city}&appid={OPENWEATHERMAP_API_KEY}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                if response.status == 200:
                    logger.info(f"Successfully fetched weather data for city: {city}")
                    return await response.json()

                elif response.status == 404:
                    logger.warning(f"City '{city}' not found. Response: {response.text()}")
                    return None

                else:
                    response_text = await response.text()
                    logger.error(
                        f"Unexpected response status {response.status} for city: {city}. Response: {response_text}"
                    )
                    raise Exception(f"Unexpected response from OpenWeather API: {response_text}")

    except Exception as e:
        logger.exception(f"An unexpected error occurred while fetching weather data for city: {city}. Error: {e}")
        return None
