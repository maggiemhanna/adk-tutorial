import sys
from pathlib import Path

# Add the project root directory to the python path to allow direct execution
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from fastapi.testclient import TestClient
from agents.root_agent.main import api
from utils.logging import setup_logging

# Setup logger
logger = setup_logging(name=__name__)

# Initialize the TestClient with our FastAPI app
client = TestClient(api)

# 1. Health check
logger.info("=== Testing Health Endpoint ===")
response = client.get("/")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
logger.info(f"Health Response: {response.json()}")

# 2. Single-turn queries
logger.info("=== Testing Single-turn Queries ===")
queries = [
    "What is the capital of France?",
    "Who wrote Hamlet?"
]
for query in queries:
    logger.info(f"Query: '{query}'")
    response = client.post("/run-root-agent", params={"query": query})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert data["status"] == "success", f"Expected success status, got {data['status']}"
    
    bot_response = data["results"]["response"]
    logger.info(f"Response: {bot_response}")

# 3. Multi-turn query (Testing session persistence)
logger.info("=== Testing Multi-turn Session ===")
# Turn 1: Provide information to remember
query_1 = "Remember this: my secret code name is Antigravity."
logger.info(f"Turn 1 Query: '{query_1}'")
response = client.post("/run-root-agent", params={"query": query_1})
assert response.status_code == 200, f"Expected 200, got {response.status_code}"

data = response.json()
assert data["status"] == "success", f"Expected success status, got {data['status']}"
session_id = data["results"]["session_id"]
logger.info(f"Turn 1 Response: {data['results']['response']}")
logger.info(f"Session ID: {session_id}")

# Turn 2: Query the information back using the same session_id
query_2 = "What did I say my secret code name was?"
logger.info(f"Turn 2 Query: '{query_2}'")
response = client.post("/run-root-agent", params={"query": query_2, "session_id": session_id})
assert response.status_code == 200, f"Expected 200, got {response.status_code}"

data = response.json()
assert data["status"] == "success", f"Expected success status, got {data['status']}"
bot_response_2 = data["results"]["response"]
logger.info(f"Turn 2 Response: {bot_response_2}")

assert "antigravity" in bot_response_2.lower(), f"Expected answer to contain 'antigravity', got: {bot_response_2}"

logger.info("All tests passed successfully!")
