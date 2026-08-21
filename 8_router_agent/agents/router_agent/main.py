from pathlib import Path
from typing import Optional, Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from agents.router_agent.agent import router_agent
from agents.hotel_agent.agent import hotel_agent
from agents.transportation_agent.agent import transportation_agent
from agents.restaurant_agent.agent import restaurant_agent

from utils.logging import setup_logging
from dotenv import load_dotenv
import json
import httpx

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

logger = setup_logging(name=__name__)

APP_NAME = "router_agent"

AGENT_ENDPOINTS = {
    "hotel_agent": "http://localhost:8001/run-hotel-agent",
    "transportation_agent": "http://localhost:8002/run-transportation-agent",
    "restaurant_agent": "http://localhost:8000/run-restaurant-agent",
}

# --- FastAPI Application ---
api = FastAPI(
    title="Router Agent Service",
    description="API for running the Router Agent."
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Core Agent Logic ---
async def setup_session_and_runner(agent, user_id: str):
    """Initializes the session service and runner for the agent."""
    service = InMemorySessionService()

    session = await service.create_session(
        app_name=agent.name, 
        user_id=user_id
    )

    runner = Runner(
        agent=agent,
        app_name=agent.name,
        session_service=service
    )

    logger.info(f"Setup session for agent: '{agent.name}', user: '{user_id}', session: '{session.id}'...")
    
    return service, session, runner

async def execute_agent_run(query: str):
    """Executes the engage agent runner and processes its responses."""
    user_id = "adk_adventurer_001"

    _, session, runner = await setup_session_and_runner(
        agent=router_agent,
        user_id=user_id
    )
    logger.info(f"Setup session for agent: '{router_agent.name}', user: '{user_id}', session: '{session.id}'...")

    responses = []
    try:
        iter = 0
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=Content(parts=[Part(text=query)], role="user")
        ):
            iter += 1
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        logger.info(f"**Iteration Event {iter}**:\n{part.text}")
                        response = json.loads(part.text)["router_response"]
                        logger.info(f"The router response is {response}")

                        if response in AGENT_ENDPOINTS:
                            endpoint = AGENT_ENDPOINTS[response]
                            logger.info(f"Calling FastAPI service for '{response}' at {endpoint}...")
                            async with httpx.AsyncClient(timeout=60.0) as client:
                                res = await client.post(endpoint, params={"query": query})
                                res.raise_for_status()
                                data = res.json()
                                bot_response = data.get("results", {}).get("response", "")
                                logger.info(f"Received response from {response}: {bot_response}")
                                responses.append(bot_response)
                        else:
                            logger.warning(f"Unknown agent response: {response}")

        return responses[-1] if responses else ""

    except Exception as e:
        logger.error(f"An error occurred during agent execution: {e}", exc_info=True)
        raise

# --- FastAPI Endpoints ---
@api.get("/")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}

@api.post("/run-router-agent", response_model=Dict[str, Any])
async def run_router_agent(query: str) -> Dict[str, Any]:
    """
    Triggers the router agent with the provided user input.
    The response will contain the structured JSON output from the agent.
    """
    logger.info(f"--- Raw User Input ---\n{query}")
    logger.info("--- Executing Agent Runner... ---")

    try:
        results = await execute_agent_run(query)
        return {
            "status": "success",
            "results": {
                "response": results
            }
        }
    except Exception:
        logger.exception("A critical error occurred while processing the request.")
        raise HTTPException(
            status_code=500, 
            detail="Internal Server Error during request processing."
        )

if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run(api, host="0.0.0.0", port=8003)