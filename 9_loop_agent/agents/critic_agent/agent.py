from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

from agents.critic_agent.prompt import system_instruction

critic_agent = Agent(
    name="critic_agent", model="gemini-2.5-flash", tools=[google_search],
    instruction=system_instruction,
    output_key="criticism"
)