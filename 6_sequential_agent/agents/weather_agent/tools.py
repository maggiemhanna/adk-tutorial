import requests
import json

from utils.logging import setup_logging

logger = setup_logging(name=__name__)

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
        
        logger.info(f"Got weather for coordinates {latitude}, {longitude}: \n{data}")
        
        return {
            "temperature": f"{current.get('temperature_2m')}°C",
            "humidity": f"{current.get('relative_humidity_2m')}%",
            "condition_code": current.get("weather_code")
        }
    except Exception as e:
        return {"error": str(e)}

# --- Main Testing Logic ---
def run_test(coords):
    logger.info(f"\n--- Testing for coordinates: {coords['latitude']}, {coords['longitude']} ---")

    # Step 2: Use Coordinates to get Weather
    logger.info(f"Calling get_weather(lat={coords['latitude']}, lon={coords['longitude']})...")
    weather = get_weather(coords['latitude'], coords['longitude'])

    if "error" in weather:
        logger.error(f"Error in Weather: {weather['error']}")
        return

    logger.info(f"Current Weather: {weather['temperature']}, Humidity: {weather['humidity']}")

if __name__ == "__main__":
    # List of test cases
    test_cases = [
        {   "latitude": 51.5074, 
            "longitude": -0.1278
        }, # London
        {   "latitude": 35.6895, 
            "longitude": 139.6917
        }, # Tokyo
        {   "latitude": 48.8566, 
            "longitude": 2.3522
        }, # Paris
        {   "latitude": 25.2048, 
            "longitude": 55.2708
        }, # Dubai
        {   "latitude": 999, 
            "longitude": 999
        }  # Error case testing
    ]

    logger.info("Starting Tool Chain Test...")
    for coords in test_cases:
        run_test(coords)
    
    logger.info("\nTests complete.")