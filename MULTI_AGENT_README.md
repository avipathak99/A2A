# A2A Multi-Agent System

This is a comprehensive A2A (Agent-to-Agent) system with multiple specialized agents that can work together.

## 🤖 Available Agents

### 1. Echo Agent (Port 9999)
- **Purpose**: Simple echo/testing agent
- **Capabilities**: Echoes back any text with "Echo: " prefix
- **Skills**: Text echoing
- **Examples**: "Hello World" → "Echo: Hello World"

### 2. Web Search Agent (Port 8001) 
- **Purpose**: Web search and information retrieval
- **Capabilities**: Searches the web using DuckDuckGo API
- **Skills**: Web search, information lookup, research
- **Examples**: 
  - "What is artificial intelligence?"
  - "Latest news about climate change"
  - "Python programming tutorial"

### 3. Calculator Agent (Port 8002)
- **Purpose**: Mathematical calculations and computations
- **Capabilities**: Basic arithmetic, advanced math functions, expression evaluation
- **Skills**: Mathematical calculations
- **Examples**:
  - "2 + 3 * 4"
  - "sqrt(16) + sin(pi/2)"
  - "Calculate the area of a circle with radius 5"

## 🚀 Quick Start

### Option 1: Easy Start (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Start all agents at once
python run_all_agents.py
```

This will start all three agents automatically. Then in a new terminal:
```bash
# Run the multi-agent client
python a2a_multi_client.py
```

### Option 2: Manual Start
Start each agent in separate terminals:

```bash
# Terminal 1 - Echo Agent
python a2a_server.py --host localhost --port 9999

# Terminal 2 - Web Search Agent  
python a2a_websearch_server.py --host localhost --port 8001

# Terminal 3 - Calculator Agent
python a2a_calculator_server.py --host localhost --port 8002

# Terminal 4 - Multi-Agent Client
python a2a_multi_client.py
```

## 🎮 Using the Multi-Agent Client

The multi-agent client (`a2a_multi_client.py`) provides several features:

### 1. **Automatic Agent Discovery**
- Discovers all running agents and their capabilities
- Shows agent cards, skills, and examples

### 2. **Smart Agent Suggestion**
- Analyzes your query and suggests the best agent
- Uses keyword matching based on agent capabilities

### 3. **Interactive Chat Interface**
- Type questions and get routed to appropriate agents
- Commands:
  - `agents` - List all discovered agents
  - `quit` - Exit the chat

### 4. **Example Demonstrations**
- Runs predefined examples to show each agent's capabilities

## 💡 Example Usage

```
💬 You: What is machine learning?
🎯 Suggested Agent: Web Search Agent
🤖 Web Search Agent: **Answer:** Machine learning is a subset of artificial intelligence...

💬 You: Calculate 15 * 23 + sqrt(144)
🎯 Suggested Agent: Calculator Agent  
🤖 Calculator Agent: **Expression:** 15 * 23 + sqrt(144)
                     **Result:** 357

💬 You: Hello there!
🎯 Suggested Agent: Echo Agent
🤖 Echo Agent: Echo: Hello there!
```

## 🔧 Architecture

### Agent Structure
Each agent follows the A2A SDK pattern:
```
Agent (Logic) → AgentExecutor (A2A Interface) → Server (HTTP/JSON-RPC)
```

### Client Architecture
```
MultiAgentClient → AgentDiscovery → ClientFactory → Individual Agents
```

### Key Features
- ✅ **Agent Discovery**: Automatic detection of available agents
- ✅ **Smart Routing**: Query analysis for optimal agent selection  
- ✅ **Agent Cards**: Standardized capability descriptions
- ✅ **Error Handling**: Graceful failure handling and recovery
- ✅ **Modern A2A SDK**: Uses proper ClientFactory and utility functions

## 🛠 Development

### Adding New Agents

1. **Create Agent Logic** (`app/new_agent.py`):
```python
class NewAgent:
    SUPPORTED_CONTENT_TYPES = ['text/plain']
    
    async def handle_text(self, text: str) -> str:
        # Your agent logic here
        return f"Processed: {text}"
```

2. **Create Agent Executor** (`app/new_agent_executor.py`):
```python
class NewAgentExecutor(AgentExecutor):
    # Follow the pattern from existing executors
```

3. **Create Server** (`a2a_new_server.py`):
```python
# Follow the pattern from existing servers
# Use a unique port number
```

4. **Update Multi-Client**:
Add your agent to the discovery list in `a2a_multi_client.py`

### Testing Individual Agents

Test each agent separately:
```bash
# Test Echo Agent
python a2a_client.py

# Test with curl
curl http://localhost:9999/.well-known/agent-card.json
```

## 📋 Dependencies

- **aiohttp**: For web search functionality
- **httpx**: HTTP client for A2A communication  
- **uvicorn**: ASGI server for hosting agents
- **click**: Command-line interface
- **a2a-python**: A2A Python SDK

## 🎯 Use Cases

1. **Multi-Modal Assistant**: Route different types of queries to specialized agents
2. **Agent Ecosystem**: Demonstrate A2A protocol capabilities
3. **Educational Tool**: Learn how different agents can collaborate
4. **Development Platform**: Base for building more complex agent systems

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Check what's using the port
   lsof -i :9999
   # Kill the process or use different ports
   ```

2. **Agent Not Responding**:
   - Check if agent server is running
   - Verify agent card URL: `http://localhost:PORT/.well-known/agent-card.json`
   - Check server logs for errors

3. **Web Search Not Working**:
   - Check internet connection
   - DuckDuckGo API may have rate limits

### Debug Mode
Run with debug logging:
```bash
export PYTHONPATH=.
python -c "import logging; logging.basicConfig(level=logging.DEBUG)" a2a_multi_client.py
```

## 🎉 Success Indicators

You'll know everything is working when:
- ✅ All agents start without errors
- ✅ Agent cards are accessible via HTTP
- ✅ Multi-client discovers all agents
- ✅ Queries get routed to appropriate agents
- ✅ Each agent returns proper responses

Happy agent building! 🚀