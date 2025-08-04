# A2A Multi-Agent Ecosystem

A comprehensive demonstration of A2A (Agent-to-Agent) protocol capabilities, from basic echo agents to fully automatic multi-agent workflows.

## 📊 **Complexity Levels Overview**

| Level | Description | Command | Features |
|-------|-------------|---------|----------|
| **Basic** | Simple Echo Agent | `python a2a_client.py` | Single agent, text echo |
| **Ecosystem** | Multi-Agent Discovery | `python a2a_discovery_client.py` | Agent cards, capabilities |
| **Interactive** | Manual Multi-Agent | `python a2a_multi_client.py` | Agent selection, coordination |
| **Automatic** | Smart Routing | `python a2a_auto_client.py` | Auto agent discovery & routing |
| **Workflows** | Orchestrated Tasks | `python a2a_auto_workflow.py` | Multi-agent workflows |

## 🚀 **Quick Start (All Levels)**

### **Prerequisites: Start All Agents**
```bash
# Install dependencies
pip install -r requirements.txt

# Install A2A SDK locally
cd a2a-python && pip install -e . && cd ..

# Start all agents (keep this running)
python run_all_agents.py
```

**Expected Output:**
```
🎮 Ready for Testing!

📝 Next Steps - Choose Your Experience:
1. 🤖 AUTOMATIC - Agents work together automatically:
   python a2a_auto_client.py
   python a2a_auto_workflow.py
2. 🌐 DISCOVERY - Explore the A2A ecosystem:
   python a2a_discovery_client.py
3. 🤝 INTERACTIVE - Manual multi-agent client:
   python a2a_multi_client.py
4. 📢 SIMPLE - Basic echo test:
   python a2a_client.py

🔍 A2A Agent Cards:
   • Echo Agent: http://localhost:9999/.well-known/agent-card.json
   • Web Search Agent: http://localhost:8001/.well-known/agent-card.json
   • Calculator Agent: http://localhost:8002/.well-known/agent-card.json
   • Registry Agent: http://localhost:8000/.well-known/agent-card.json
   • Coordinator Agent: http://localhost:8003/.well-known/agent-card.json
```

---

## 📢 **LEVEL 1: Basic Echo Agent**

**Complexity:** Beginner  
**Purpose:** Learn basic A2A client-server communication

### **Commands:**
```bash
# Option A: Simple client test
python a2a_client.py

# Option B: Manual server + client
python a2a_server.py --host localhost --port 9999    # Terminal 1
python a2a_client.py                                   # Terminal 2
```

### **What It Does:**
- Connects to Echo Agent via A2A protocol
- Sends "Hello A2A World!" message
- Receives echoed response with prefix

### **Expected Output:**
```
INFO: Fetching agent card from: http://localhost:9999/.well-known/agent-card.json
INFO: Successfully fetched agent card: Echo Agent
INFO: A2A Client initialized using ClientFactory.
INFO: Sending message to Echo Agent...

Agent response: Echo: Hello A2A World!
Sending another message...
Agent response: Echo: This is a test message!
```

### **Key Learning:**
- A2A protocol basics
- Agent card discovery
- Message formatting
- Client-server interaction

---

## 🌐 **LEVEL 2: Ecosystem Discovery**

**Complexity:** Intermediate  
**Purpose:** Explore the full A2A ecosystem and agent capabilities

### **Commands:**
```bash
python a2a_discovery_client.py
```

### **What It Does:**
- Discovers all A2A agents in ecosystem
- Shows detailed agent cards and capabilities
- Demonstrates A2A protocol features
- Interactive agent testing

### **Expected Output:**
```
🌐 A2A Ecosystem Discovery

🔍 DISCOVERED AGENTS:
1. 📢 Echo Agent (http://localhost:9999/)
   🎯 Capabilities: Streaming ✅, Push Notifications ✅
   🏷️  Skills: Echo Skill, A2A Protocol Testing
   📝 Description: A foundational A2A agent that echoes back messages...

2. 🔍 Web Search Agent (http://localhost:8001/)
   🎯 Capabilities: Streaming ✅, Push Notifications ✅
   🏷️  Skills: Web Search, Information Retrieval
   📝 Description: A specialized A2A agent for web searches...

3. 🧮 Calculator Agent (http://localhost:8002/)
   🎯 Capabilities: Streaming ✅, Push Notifications ✅
   🏷️  Skills: Calculate, Mathematical Functions
   📝 Description: A mathematical computation A2A agent...

Interactive Commands:
- 'agents' - List all agents
- 'test <agent_number>' - Test specific agent
- 'demo' - Run A2A protocol demonstration
- 'session' - Start interactive A2A session
```

### **Key Learning:**
- Agent discovery via A2A protocol
- Agent capabilities and skills
- A2A card structure
- Interactive testing

---

## 🤝 **LEVEL 3: Interactive Multi-Agent**

**Complexity:** Intermediate-Advanced  
**Purpose:** Manually select and coordinate multiple agents

### **Commands:**
```bash
python a2a_multi_client.py
```

### **What It Does:**
- Lists all available agents
- Allows manual agent selection
- Coordinates tasks across multiple agents
- Shows agent responses and capabilities

### **Expected Output:**
```
🤝 Multi-Agent A2A Client

📋 Available Agents:
1. Echo Agent - Testing and echo functionality
2. Web Search Agent - Web search and information retrieval  
3. Calculator Agent - Mathematical calculations and computations
4. Registry Agent - Agent discovery and registry management
5. Coordinator Agent - Multi-agent coordination and orchestration

🎯 Agent Query: 2
💬 Query: What is machine learning?

🔍 Contacting Web Search Agent...
🔍 Web Search Results:
**Query:** What is machine learning?
**Answer:** Machine learning is a method of data analysis that automates analytical model building...

🎯 Agent Query: 3  
💬 Query: Calculate 2^8

🧮 Contacting Calculator Agent...
🧮 Calculator Results:
**Expression:** 2^8
**Result:** 256
```

### **Key Learning:**
- Manual agent selection
- Multi-agent coordination
- Understanding agent specializations
- Task distribution strategies

---

## 🤖 **LEVEL 4: Automatic Agent Usage**

**Complexity:** Advanced  
**Purpose:** Experience fully automatic agent discovery and routing

### **Commands:**
```bash
python a2a_auto_client.py
```

### **Interactive Mode Options:**
```bash
Choose demonstration mode:
1. Full demonstration (recommended)    # See everything
2. Interactive automatic mode only     # Just query naturally  
3. Workflow examples only             # See automatic workflows
```

### **What It Does:**
- **Auto-discovers** all A2A agents
- **Automatically routes** queries to best agent
- **Intelligent pattern recognition** for query analysis
- **Natural language** interface - no agent selection needed

### **Example Queries & Automatic Routing:**
```bash
🤖 Auto-Query: Hello world
🎯 Auto-routing to Echo Agent
📝 Reason: Matched keywords: ['test_detected'] (score: 3.3)
🤖 Auto-Response: Echo: Hello world

🤖 Auto-Query: Calculate 15 * 23 + sqrt(144)
🎯 Auto-routing to Calculator Agent
📝 Reason: Matched keywords: ['math_detected'] (score: 5.8)
🤖 Auto-Response: 🧮 Calculator Results: **Result:** 357

🤖 Auto-Query: What is artificial intelligence?
🎯 Auto-routing to Web Search Agent
📝 Reason: Matched keywords: ['search_detected'] (score: 5.7)
🤖 Auto-Response: 🔍 Web Search Results: **Answer:** Artificial intelligence is...

🤖 Auto-Query: Find agents that can calculate
🎯 Auto-routing to Registry Agent
📝 Reason: Matched keywords: ['discovery'] (score: 4.6)
🤖 Auto-Response: 📊 Available calculation agents: Calculator Agent...
```

### **Key Learning:**
- Automatic agent discovery
- Intelligent query routing
- Pattern recognition systems
- Natural language interfaces
- Fallback mechanisms

---

## 🔄 **LEVEL 5: Automatic Workflows**

**Complexity:** Expert  
**Purpose:** Orchestrate complex multi-agent workflows automatically

### **Commands:**
```bash
python a2a_auto_workflow.py
```

### **Demonstration Options:**
```bash
Choose demonstration:
1. 🔄 Full automatic workflow demonstration
2. 🧠 Automatic intelligence showcase  
3. 🎮 Interactive automatic mode
4. 🚀 All demonstrations
```

### **Predefined Automatic Workflows:**

#### **Research & Calculate Workflow:**
```bash
🔄 Executing Automatic Workflow: research_calculate

Step 1/3: websearch → "What is the golden ratio?"
🎯 Auto-routing to Web Search Agent
✅ Response: The golden ratio is a mathematical constant approximately equal to 1.618...

Step 2/3: calculator → "Calculate (1 + sqrt(5)) / 2"  
🎯 Auto-routing to Calculator Agent
✅ Response: **Expression:** (1 + sqrt(5)) / 2 **Result:** 1.618033988749895

Step 3/3: echo → "Golden ratio research and calculation complete"
🎯 Auto-routing to Echo Agent
✅ Response: Echo: Golden ratio research and calculation complete

🎉 Workflow 'research_calculate' completed!
📈 Success rate: 3/3
```

#### **Dynamic Workflow Creation:**
```bash
🧠 Creating Dynamic Workflow from: Find information about machine learning and calculate some statistics

📋 Workflow Analysis: Breaking down into search and calculation components...

Dynamic Step 1/3: Auto-selected Agent: websearch
💬 Auto-generated Query: Search for information about: Find information about machine learning and calculate some statistics
✅ Auto-Response: Machine learning is a subset of artificial intelligence...

Dynamic Step 2/3: Auto-selected Agent: calculator  
💬 Auto-generated Query: Calculate something related to: Find information about machine learning and calculate some statistics
✅ Auto-Response: 🧮 Statistics calculation complete...

Dynamic Step 3/3: Auto-selected Agent: coordinator
💬 Auto-generated Query: Coordinate response for: Find information about machine learning and calculate some statistics
✅ Auto-Response: 🤝 Coordinated machine learning research with statistical analysis complete.
```

### **Interactive Workflow Commands:**
```bash
🤖 Workflow Command: list
🔄 Available Automatic Workflows:
- research_calculate (3 steps)
- math_research (4 steps)  
- discovery_test (5 steps)
- problem_solving (4 steps)

🤖 Workflow Command: run research_calculate
🤖 Workflow Command: create "Research quantum computing and calculate some physics equations"
🤖 Workflow Command: all
🤖 Workflow Command: quit
```

### **Key Learning:**
- Multi-agent orchestration
- Automatic workflow creation
- Dynamic task decomposition
- Complex coordination patterns
- A2A ecosystem utilization

---

## 🏗️ **Architecture Overview**

### **Agents in the Ecosystem:**

| Agent | Port | Purpose | Skills |
|-------|------|---------|--------|
| **Echo Agent** | 9999 | Testing & A2A protocol validation | echo_skill, a2a_testing |
| **Web Search Agent** | 8001 | Information retrieval | web_search, information_retrieval |
| **Calculator Agent** | 8002 | Mathematical computations | calculate, mathematical_functions, computation_service |
| **Registry Agent** | 8000 | Agent discovery & management | agent_discovery, agent_listing, registry_management |
| **Coordinator Agent** | 8003 | Multi-agent orchestration | coordinate_agents, multi_agent_tasks, orchestration |

### **A2A Protocol Features Demonstrated:**

- ✅ **Agent Discovery**: Via `.well-known/agent-card.json`
- ✅ **Capability Declaration**: Skills, content types, streaming
- ✅ **Message Routing**: Based on agent capabilities
- ✅ **Task Management**: Status tracking, history, context
- ✅ **Error Handling**: Graceful failure and recovery
- ✅ **Streaming Support**: Real-time communication
- ✅ **Push Notifications**: Event-driven updates

### **Client Libraries Used:**

- `A2ACardResolver` - Agent discovery
- `ClientFactory` - Modern client creation
- `ClientConfig` - Transport configuration
- `create_text_message_object` - Message formatting
- `get_message_text` - Response parsing

---

## 🎯 **Learning Path Recommendations**

### **For Beginners:**
1. Start with **Level 1** (Basic Echo) - Learn A2A fundamentals
2. Move to **Level 2** (Discovery) - Understand agent ecosystem
3. Try **Level 3** (Interactive) - Manual coordination experience

### **For Intermediate:**
1. Jump to **Level 4** (Automatic) - See intelligent routing
2. Explore **Level 5** (Workflows) - Complex orchestration

### **For Advanced:**
1. Study the automatic routing logic in `app/intelligent_router.py`
2. Examine workflow management in `app/auto_workflow_manager.py`
3. Create custom agents and integrate into ecosystem

---

## 📚 **Additional Resources**

### **Documentation Files:**
- `AUTOMATIC_A2A_README.md` - Detailed automatic system guide
- `A2A_ECOSYSTEM_README.md` - Complete ecosystem documentation
- `MULTI_AGENT_README.md` - Multi-agent interaction guide
- `DIFFERENCES.md` - SDK usage clarifications

### **Example Commands Quick Reference:**
```bash
# Basic testing
python a2a_client.py

# Ecosystem exploration  
python a2a_discovery_client.py

# Manual multi-agent
python a2a_multi_client.py

# Automatic routing
python a2a_auto_client.py

# Automatic workflows
python a2a_auto_workflow.py

# Start all agents
python run_all_agents.py
```

### **Troubleshooting:**
```bash
# Check if agents are running
curl http://localhost:9999/.well-known/agent-card.json
curl http://localhost:8001/.well-known/agent-card.json
curl http://localhost:8002/.well-known/agent-card.json

# Restart all agents
# Press Ctrl+C in run_all_agents.py terminal, then restart
python run_all_agents.py
```

---

## 🎉 **What You'll Learn**

By working through all levels, you'll understand:

- **A2A Protocol Fundamentals** - How agents communicate
- **Agent Discovery** - Finding and connecting to agents
- **Capability Declaration** - How agents advertise skills
- **Message Routing** - Directing queries to appropriate agents
- **Automatic Intelligence** - Pattern recognition and smart routing
- **Multi-Agent Coordination** - Orchestrating complex workflows
- **Ecosystem Design** - Building interconnected agent systems

**Start simple, progress to complex, master the A2A protocol! 🚀**