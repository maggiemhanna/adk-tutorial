from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

from agents.planner_agent.prompt import system_instruction

planner_agent = Agent(
    name="planner_agent", model="gemini-2.5-flash", tools=[google_search],
    instruction=system_instruction,
    output_key="current_plan"
)