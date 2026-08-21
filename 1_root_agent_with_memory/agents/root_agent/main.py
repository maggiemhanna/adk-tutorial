# Copyright (c) 2024 Maggie Mhanna
# All rights reserved.

import os
from pathlib import Path
from typing import Any, Dict, Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# --- Load Environment Variables ---
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# We import root_agent AFTER loading environment variables in case it initializes tools or models
# that depend on env vars immediately.
from agents.root_agent import root_agent
from utils.logging import setup_logging

# --- Configuration & Setup ---
logger = setup_logging(name=__name__)

APP_NAME = "root_agent"

# --- FastAPI Application ---
api = FastAPI(
    title="Root Agent",
    description="API for running the Root Agent."
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get("/", tags=["Health"])
async def root() -> Dict[str, str]:
    return {"message": "Root Agent is running. Use the /run-root-agent endpoint via POST."}

# --- Core Agent Logic ---
service = InMemorySessionService()

async def setup_session_and_runner(user_id: str, session_id: Optional[str] = None):
    """Initializes the session service and runner for the agent."""
    if session_id is None:
        session = await service.create_session(
            app_name=root_agent.name, 
            user_id=user_id
        )
        session_id = session.id
        logger.info(f"Created new session for user '{user_id}': '{session_id}'")
    else:
        logger.info(f"Using existing session for user '{user_id}': '{session_id}'")

    runner = Runner(
        agent=root_agent,
        app_name=root_agent.name,
        session_service=service
    )

    logger.info(f"Setup session for agent: '{root_agent.name}', user: '{user_id}', session: '{session_id}'...")
    
    return session_id, runner

async def execute_agent_run(query: str, session_id: Optional[str] = None):
    """Executes the engage agent runner and processes its responses."""
    user_id = "root_agent_user_001"

    session_id, runner = await setup_session_and_runner(
        user_id=user_id,
        session_id=session_id
    )

    final_response = ""
    try:
        iter_count = 0
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(parts=[types.Part(text=query)], role="user")
        ):
            iter_count += 1
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        logger.info(f"**Iteration Event {iter_count}**:\n{part.text}")
                        final_response += part.text

    except Exception as e:
        logger.error(f"An error occurred during agent execution: {e}", exc_info=True)
        raise

    return session_id, final_response


# --- FastAPI Endpoints ---
@api.post("/run-root-agent", response_model=Dict[str, Any], tags=["Agent"])
async def run_root_agent(query: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Triggers the flights search agent with the provided user input.
    The response will contain the structured JSON output from the agent.
    """
    logger.info(f"--- Raw User Query ---\n{query}")
    logger.info("--- Executing Agent Runner... ---")

    try:
        session_id_out, response_text = await execute_agent_run(query, session_id)
        return {
            "status": "success",
            "results": {
                "session_id": session_id_out,
                "response": response_text
            }
        }
    except Exception:
        logger.exception("A critical error occurred while processing the request.")
        raise HTTPException(
            status_code=500, 
            detail="Internal Server Error during request processing."
        )

# --- Running the Server ---
if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run(api, host="127.0.0.1", port=8000)