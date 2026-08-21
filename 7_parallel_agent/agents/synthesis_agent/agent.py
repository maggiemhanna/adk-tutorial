from google.adk.agents.llm_agent import Agent
from agents.synthesis_agent.prompt import system_instruction

synthesis_agent = Agent(
    model="gemini-2.5-flash",
    name='synthesis_agent',
    description="An agent workflow that finds multiple things in parallel and then synthesizes the results.",
    instruction=system_instruction,
)