from google.adk.agents.llm_agent import Agent

from agents.hotel_agent.prompt import system_instruction

hotel_agent = Agent(
    model='gemini-2.5-flash',
    name='hotel_agent',
    description='An agent that answers user questions about hotel availability in a given location.',
    instruction=system_instruction,
)
