from google.adk.agents.llm_agent import Agent


from agents.root_agent.prompt import system_instruction
from agents.hotel_agent.agent import hotel_agent
from agents.restaurant_agent.agent import restaurant_agent
from agents.transportation_agent.agent import transportation_agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='An agent that delegatese other agent to answer user questions.',
    instruction=system_instruction,
    sub_agents=[hotel_agent, restaurant_agent, transportation_agent],
)
