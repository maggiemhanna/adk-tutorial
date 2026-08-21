from google.adk.agents.llm_agent import Agent

from agents.location_agent.tools import get_coordinates
from agents.location_agent.prompt import system_instruction
from agents.location_agent.schema import LocationAgentOutput

location_agent = Agent(
    model='gemini-2.5-flash',
    name='location_agent',
    description='A helpful assistant that answers user questions about the coordinates of a location.',
    instruction=system_instruction,
    tools=[get_coordinates],
    output_schema=LocationAgentOutput
)
