# Copyright (c) 2024 Maggie Mhanna
# All rights reserved.

import json
import os
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from agents.customer_support_triage.agent import customer_support_triage
from agents.customer_support_triage.schema import SupportTicketInput, SupportTriageOutput

from dotenv import load_dotenv

from utils.logging import format_dict_for_logs, setup_logging

# --- Configuration & Setup ---
load_dotenv(Path(__file__).parent / ".env")
logger = setup_logging(name=__name__)

APP_NAME = "customer_support_triage"

# --- FastAPI Application ---
api = FastAPI(
    title="Customer Support Triage Agent Service",
    description="API for running the Customer Support Triage Agent."
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
    return {"message": "Customer Support Triage Agent Service is running. Use the /run-customer-support-triage endpoint via POST."}

# --- Core Agent Logic ---
service = InMemorySessionService()

async def setup_session_and_runner(session_id: str, user_id: str, initial_state: dict):
    """Initializes the session service and runner for the agent."""

    session = await service.create_session(
        app_name=APP_NAME, 
        user_id=user_id, 
        session_id=session_id, 
        state=initial_state
    )

    runner = Runner(
        agent=customer_support_triage,
        app_name=APP_NAME,
        session_service=service
    )
    return service, session, runner

async def execute_agent_run(ticket_input: SupportTicketInput) -> Dict[str, Any]:
    """Executes the customer support triage agent runner and processes its responses."""
    
    session_id = str(uuid4())
    user_id = str(uuid4())  # Generate per-request rather than globally
    initial_state = ticket_input.model_dump()

    _, _, runner = await setup_session_and_runner(
        session_id=session_id, 
        user_id=user_id,
        initial_state=initial_state
    )

    try:
        responses = await runner.run_debug(
            "Follow the system instructions.", 
            user_id=user_id, 
            session_id=session_id,
            quiet=True
        )
        
        parsed_responses =[]
        for resp in responses:
            text_content = resp.content.parts[-1].text
            try:
                parsed_responses.append(json.loads(text_content))
            except json.JSONDecodeError:
                logger.warning("Agent response text was not valid JSON. Returning raw text.")
                parsed_responses.append({"raw_text": text_content})
        
        logger.info(f"--- Agent Response ---\n{format_dict_for_logs(parsed_responses)}")
        return parsed_responses

    except Exception as e:
        logger.error(f"An error occurred during agent execution: {e}", exc_info=True)
        raise

# --- FastAPI Endpoints ---
@api.post("/run-customer-support-triage", response_model=Dict[str, Any], tags=["Agent"])
async def run_customer_support_triage(ticket_input: SupportTicketInput) -> Dict[str, Any]:
    """
    Triggers the customer support triage agent with the provided user input.
    The response will contain the structured JSON output from the agent.
    """
    logger.info(f"--- Raw User Input ---\n{format_dict_for_logs(ticket_input.model_dump())}")
    logger.info("--- Executing Agent Runner... ---")

    try:
        results = await execute_agent_run(ticket_input)
        return {
            "status": "success",
            "results": results
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