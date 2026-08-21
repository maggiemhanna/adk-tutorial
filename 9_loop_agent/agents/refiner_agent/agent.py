from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.tools import ToolContext

from agents.refiner_agent.prompt import system_instruction

def exit_loop(tool_context: ToolContext):
  """Call this function ONLY when the plan is approved, signaling the loop should end."""
  print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
  tool_context.actions.escalate = True
  return {}

refiner_agent = Agent(
    name="refiner_agent", model="gemini-2.5-flash", tools=[exit_loop],
    instruction=system_instruction,
    output_key="current_plan"
)