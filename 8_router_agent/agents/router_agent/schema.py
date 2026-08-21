from pydantic import BaseModel, Field
from typing import Literal

class RouterAgentOutput(BaseModel):
    router_response: Literal["hotel_agent", "transportation_agent", "restaurant_agent"] = Field(..., description="The decision of the router agent.")

