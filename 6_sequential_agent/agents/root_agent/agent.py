from google.adk.agents.sequential_agent import SequentialAgent

from agents.location_agent.agent import location_agent
from agents.weather_agent.agent import weather_agent

root_agent = SequentialAgent(
    name='root_agent',
    description='A Workflow that answers user questions about the weather for specific location using available subagents.',
    sub_agents=[location_agent, weather_agent],
)
