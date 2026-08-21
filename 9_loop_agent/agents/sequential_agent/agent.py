from google.adk.agents.sequential_agent import SequentialAgent

from agents.planner_agent.agent import planner_agent
from agents.loop_agent.agent import loop_agent

sequential_agent = SequentialAgent(
    name="sequential_agent",
    sub_agents=[planner_agent, loop_agent],
    description="A workflow that iteratively plans and refines a trip to meet constraints."
)