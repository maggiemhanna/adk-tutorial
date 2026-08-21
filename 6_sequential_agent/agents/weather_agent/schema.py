from pydantic import BaseModel, Field

class WeatherAgentInput(BaseModel):
    """Input schema for the weather agent."""
    latitude: float = Field(description='Latitude of the location.')
    longitude: float = Field(description='Longitude of the location.')
    