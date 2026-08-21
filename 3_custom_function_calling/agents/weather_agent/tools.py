import requests
import json

from utils.logging import setup_logging

logger = setup_logging(name=__name__)

# --- Function 1: Geocoding ---
def get_coordinates(location: str):
    """Get latitude and longitude for a string location.

    Args:
        location (str): The location to get the coordinates for.

    Returns:
        dict: A dictionary containing the latitude, longitude, name, and country of the location.
    """

    logger.info(f"Getting coordinates for location: {location}")
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": location, "count": 1, "language": "en", "format": "json"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("results"):
            return {"error": f"Location '{location}' not found."}
        
        result = data["results"][0]
        
        logger.info(f"The coordinates for {location} are: latitude: {result['latitude']}, longitude: {result['longitude']}")
        results = {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "name": result["name"],
            "country": result.get("country")
        }
        logger.info(f"The coordinates for {location} are: \n {results}")
        return results

    except Exception as e:
        return {"error": str(e)}

# --- Function 2: Weather ---
def get_weather(latitude: float, longitude: float):
    """Get weather for specific coordinates.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

    Returns:
        dict: A dictionary containing the temperature, humidity, and condition code of the location.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "weather_code"],
        "timezone": "auto"
    }
    logger.info(f"Getting weather for coordinates: {latitude}, {longitude}")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        current = data.get("current", {})
        
        logger.info(f"Got weather for coordinates {latitude}, {longitude}")
        results = {
            "temperature": f"{current.get('temperature_2m')}°C",
            "humidity": f"{current.get('relative_humidity_2m')}%",
            "condition_code": current.get("weather_code")
        }
        logger.info(f"The weather for coordinates ({latitude}, {longitude}) is: \n {results}")
        
        return results

    except Exception as e:
        return {"error": str(e)}

# --- Main Testing Logic ---
def run_test(location_name):
    logger.info(f"\n--- Testing for: {location_name} ---")
    
    # Step 1: Get Coordinates
    logger.info(f"Step 1: Calling get_coordinates('{location_name}')...")
    coords = get_coordinates(location_name)
    
    if "error" in coords:
        logger.error(f"Error in Geocoding: {coords['error']}")
        return

    logger.info(f"Found: {coords['name']}, {coords['country']} ({coords['latitude']}, {coords['longitude']})")

    # Step 2: Use Coordinates to get Weather
    logger.info(f"Step 2: Calling get_weather(lat={coords['latitude']}, lon={coords['longitude']})...")
    weather = get_weather(coords['latitude'], coords['longitude'])

    if "error" in weather:
        logger.error(f"Error in Weather: {weather['error']}")
        return

    logger.info(f"Current Weather: {weather['temperature']}, Humidity: {weather['humidity']}")

if __name__ == "__main__":
    # List of test cases
    test_cases = [
        "London",          # Standard city
        "Tokyo",           # Different continent
        "Paris",           # Common name
        "Dubai",           # Extreme climate
        "NotARealPlace123" # Error case testing
    ]

    logger.info("Starting Tool Chain Test...")
    for city in test_cases:
        run_test(city)
    
    logger.info("\nTests complete.")