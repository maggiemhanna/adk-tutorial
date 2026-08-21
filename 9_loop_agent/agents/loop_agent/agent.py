from google.adk.agents.loop_agent import LoopAgent

from agents.critic_agent.agent import critic_agent
from agents.refiner_agent.agent import refiner_agent

loop_agent = LoopAgent(
    name="loop_agent",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=3
)