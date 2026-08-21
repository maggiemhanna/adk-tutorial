const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const AGENT_API_URL = process.env.AGENT_API_URL || 'http://127.0.0.1:8000';

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Proxy endpoint to communicate with the FastAPI backend
app.post('/api/chat', async (req, res) => {
  const { query, session_id } = req.body;
  if (!query) {
    return res.status(400).json({ error: 'Query is required' });
  }

  try {
    const url = new URL(`${AGENT_API_URL}/run-root-agent`);
    url.searchParams.append('query', query);
    if (session_id) {
      url.searchParams.append('session_id', session_id);
    }

    const response = await fetch(url.toString(), {
      method: 'POST',
      headers: {
        'Accept': 'application/json'
      }
    });

    if (!response.ok) {
      const errorText = await response.text();
      return res.status(response.status).json({ error: errorText || 'Failed to call agent api' });
    }

    const data = await response.json();
    res.json(data);
  } catch (error) {
    console.error('Error forwarding request to agent API:', error);
    res.status(500).json({ error: 'Internal Server Error forwarding request to agent' });
  }
});

app.listen(PORT, () => {
  console.log(`Frontend server is running on http://localhost:${PORT}`);
});
