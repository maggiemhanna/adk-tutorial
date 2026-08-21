from google.adk.agents.llm_agent import Agent
from google.adk.tools import ToolContext
from google.adk.tools.agent_tool import AgentTool

from agents.weather_agent.tools import get_weather
from agents.weather_agent.prompt import system_instruction

weather_agent = Agent(
    model='gemini-2.5-flash',
    name='weather_agent',
    description='A helpful assistant that answers user questions about the weather for a specific coordinates.',
    instruction=system_instruction,
    tools=[get_weather],
)

async def call_weather_agent(
    query: str,
    tool_context: ToolContext,
):
    """
    After getting data with call_location_agent, use this tool to check the weather for the coordinates sent back.
    """
    print("--- TOOL CALL: call_weather_agent ---")
    # Retrieve the data fetched by the previous tool
    coordinates = tool_context.state.get("coordinates", "No data found.")

    # Formulate a new prompt for the weather agent, giving it the coordinates context
    query_with_data = f"""
    Context: The coordinates for the location in question are: {coordinates}

    User's Request: {query}
    """

    agent_tool = AgentTool(agent=weather_agent)
    weather_agent_output = await agent_tool.run_async(
        args={"request": query_with_data}, tool_context=tool_context
    )
    
    # Store the retrieved data in the context's state
    tool_context.state["weather"] = weather_agent_output
    return weather_agent_output