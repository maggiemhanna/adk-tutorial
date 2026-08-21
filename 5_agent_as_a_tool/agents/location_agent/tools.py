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
        
        logger.info(f"Found coordinates for location {location}: \n{result}")
        return {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "name": result["name"],
            "country": result.get("country")
        }
    except Exception as e:
        return {"error": str(e)}


# --- Main Testing Logic ---
def run_test(location_name):
    logger.info(f"\n--- Testing for: {location_name} ---")
    
    # Step 1: Get Coordinates
    logger.info(f"Calling get_coordinates('{location_name}')...")
    coords = get_coordinates(location_name)
    
    if "error" in coords:
        logger.error(f"Error in Geocoding: {coords['error']}")
        return

    logger.info(f"Found: {coords['name']}, {coords['country']} ({coords['latitude']}, {coords['longitude']})")

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