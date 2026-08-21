from typing import Literal, List
from pydantic import BaseModel, Field

class LocationAgentOutput(BaseModel):
    """Output schema for the location agent."""
    latitude: float = Field(description='Latitude of the location.')
    longitude: float = Field(description='Longitude of the location.')
    