import sys
from pathlib import Path

# Add the project root directory to the python path to allow direct execution
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from fastapi.testclient import TestClient
from agents.router_agent.main import api
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
    "How can I get from New York to Los Angeles?",
    "I'm traveling to Los Angeles, find me a hotel to stay in.",
    "I'm traveling to Los Angeles, what are some restaurants I can visit that offer vegan food?"
]
for query in queries:
    logger.info(f"Query: '{query}'")
    response = client.post("/run-router-agent", params={"query": query})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert data["status"] == "success", f"Expected success status, got {data['status']}"
    
    bot_response = data["results"]["response"]
    logger.info(f"Response: {bot_response}")
