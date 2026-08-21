from pathlib import Path
from typing import Optional, Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from agents.root_agent.agent import root_agent
from utils.logging import setup_logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

logger = setup_logging(name=__name__)

APP_NAME = "root_agent"

# --- FastAPI Application ---
api = FastAPI(
    title="Root Agent Service",
    description="API for running the Root Agent."
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Core Agent Logic ---
async def setup_session_and_runner(user_id: str):
    """Initializes the session service and runner for the agent."""
    service = InMemorySessionService()

    session = await service.create_session(
        app_name=root_agent.name, 
        user_id=user_id
    )

    runner = Runner(
        agent=root_agent,
        app_name=root_agent.name,
        session_service=service
    )

    logger.info(f"Setup session for agent: '{root_agent.name}', user: '{user_id}', session: '{session.id}'...")
    
    return service, session, runner

async def execute_agent_run(query: str):
    """Executes the engage agent runner and processes its responses."""
    user_id = "adk_adventurer_001"

    _, session, runner = await setup_session_and_runner(
        user_id=user_id
    )
    logger.info(f"Setup session for agent: '{root_agent.name}', user: '{user_id}', session: '{session.id}'...")

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
                        responses.append(part.text)

        return responses[-1] if responses else ""

    except Exception as e:
        logger.error(f"An error occurred during agent execution: {e}", exc_info=True)
        raise

# --- FastAPI Endpoints ---
@api.get("/")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}

@api.post("/run-root-agent", response_model=Dict[str, Any])
async def run_root_agent(query: str) -> Dict[str, Any]:
    """
    Triggers the root agent with the provided user input.
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
    uvicorn.run(api, host="0.0.0.0", port=8002)