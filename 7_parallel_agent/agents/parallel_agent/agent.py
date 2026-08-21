from google.adk.agents.parallel_agent import ParallelAgent


from agents.hotel_agent.agent import hotel_agent
from agents.restaurant_agent.agent import restaurant_agent
from agents.transportation_agent.agent import transportation_agent

parallel_agent = ParallelAgent(
    name='parallel_agent',
    sub_agents=[hotel_agent, restaurant_agent, transportation_agent],
)
