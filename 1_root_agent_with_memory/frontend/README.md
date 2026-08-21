# ADK Root Agent Chatbot Frontend

A premium, modern chatbot user interface built using Node.js, Express, HTML, and CSS to interact with the ADK Root Agent backend.

## Features
- **Modern Chatbot Interface**: Styled with custom dark-theme glassmorphism and animations.
- **Session Management**: Automatically generates new session IDs, allows copying current session ID to clipboard, starting new sessions, or reloading/resuming existing sessions.
- **Express Proxy**: Proxy endpoint requests seamlessly to the FastAPI backend.

## Prerequisites
- Node.js (v18+)
- Python 3 with dependencies in `requirements.txt` installed.

## Running the Application

### 1. Start the FastAPI Backend
From the root project directory, run:
```bash
python3 -m agents.root_agent.main
```
The backend will run on `http://127.0.0.1:8000`.

### 2. Start the Node.js Frontend
From the `frontend` directory, run:
```bash
npm install
npm start
```
The frontend will run on `http://localhost:3000`.

Open your browser and navigate to `http://localhost:3000` to start chatting!
