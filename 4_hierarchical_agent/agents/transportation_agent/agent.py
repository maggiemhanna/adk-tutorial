from google.adk.agents.llm_agent import Agent

from agents.transportation_agent.prompt import system_instruction

transportation_agent = Agent(
    model='gemini-2.5-flash',
    name='transportation_agent',
    description='An agent that answers user questions about transportation options for getting from one location to another location.',
    instruction=system_instruction,
)
