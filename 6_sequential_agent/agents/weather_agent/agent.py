from google.adk.agents.llm_agent import Agent

from agents.weather_agent.tools import get_weather
from agents.weather_agent.prompt import system_instruction
from agents.weather_agent.schema import WeatherAgentInput

weather_agent = Agent(
    model='gemini-2.5-flash',
    name='weather_agent',
    description='A helpful assistant that answers user questions about the weather for a specific coordinates.',
    instruction=system_instruction,
    tools=[get_weather],
    input_schema=WeatherAgentInput
)
