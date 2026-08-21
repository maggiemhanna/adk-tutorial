from google.adk.agents.sequential_agent import SequentialAgent

from agents.parallel_agent.agent import parallel_agent
from agents.synthesis_agent.agent import synthesis_agent

sequential_agent = SequentialAgent(
    name='sequential_agent',
    sub_agents=[parallel_agent, synthesis_agent],
    description="An agent workflow that finds multiple things in parallel and then synthesizes the results."
)
