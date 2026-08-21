from google.adk.agents.llm_agent import Agent

from agents.router_agent.prompt import system_instruction
from agents.router_agent.schema import RouterAgentOutput


router_agent = Agent(
    model='gemini-2.5-flash',
    name='router_agent',
    description='An agent that routes user questions to the appropriate sub-agent based on the user\'s intent.',
    instruction=system_instruction,
    output_schema=RouterAgentOutput,
)
