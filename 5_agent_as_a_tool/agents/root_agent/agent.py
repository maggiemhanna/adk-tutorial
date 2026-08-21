from google.adk.agents.llm_agent import Agent


from agents.root_agent.prompt import system_instruction
from agents.location_agent.agent import call_location_agent
from agents.weather_agent.agent import call_weather_agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant that answers user questions about the weather for specific location using available subagents.',
    instruction=system_instruction,
    tools=[call_location_agent, call_weather_agent],
)
