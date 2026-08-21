from google.adk.agents.llm_agent import Agent

from agents.restaurant_agent.prompt import system_instruction

restaurant_agent = Agent(
    model='gemini-2.5-flash',
    name='restaurant_agent',
    description='A helpful assistant that retrieves restaurant recommendations based on cuisine type and optionally a location.',
    instruction=system_instruction,
    output_key="restaurant_results"
)
