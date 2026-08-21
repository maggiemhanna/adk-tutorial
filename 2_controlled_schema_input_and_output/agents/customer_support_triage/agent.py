from google.adk.agents.llm_agent import Agent
from agents.customer_support_triage.prompt import system_instruction
from agents.customer_support_triage.schema import SupportTriageOutput

customer_support_triage = Agent(
    model='gemini-2.5-flash',
    name='customer_support_triage',
    description='An intelligent agent for triaging customer support tickets.',
    instruction=system_instruction,
    output_schema=SupportTriageOutput,
)
