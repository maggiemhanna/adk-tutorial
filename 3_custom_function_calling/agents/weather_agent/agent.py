from google.adk.agents.llm_agent import Agent

from agents.weather_agent.tools import get_coordinates, get_weather
from agents.weather_agent.prompt import system_instruction

weather_agent = Agent(
    model='gemini-2.5-flash',
    name='weather_agent',
    description='A helpful assistant that answers user questions about the weather.',
    instruction=system_instruction,
    tools=[get_coordinates, get_weather],
)
