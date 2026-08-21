from google.adk.agents.llm_agent import Agent
from google.adk.tools import ToolContext
from google.adk.tools.agent_tool import AgentTool

from agents.location_agent.tools import get_coordinates
from agents.location_agent.prompt import system_instruction

location_agent = Agent(
    model='gemini-2.5-flash',
    name='location_agent',
    description='A helpful assistant that answers user questions about the coordinates of a location.',
    instruction=system_instruction,
    tools=[get_coordinates],
)

async def call_location_agent(
    query: str,
    tool_context: ToolContext,
):
    """
    Use this tool to get the coordinates of a location.
    """
    print("--- TOOL CALL: call_location_agent ---")
    agent_tool = AgentTool(agent=location_agent)
    location_agent_output = await agent_tool.run_async(
        args={"request": query}, tool_context=tool_context
    )
    # Store the retrieved data in the context's state
    tool_context.state["coordinates"] = location_agent_output
    return location_agent_output