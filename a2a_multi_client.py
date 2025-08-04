"""Multi-Agent A2A Client - Discovers and uses different agents based on capabilities."""

import asyncio
import logging
from typing import Dict, List, Optional

import httpx

from a2a.client import A2ACardResolver, ClientFactory, ClientConfig
from a2a.client.helpers import create_text_message_object
from a2a.types import AgentCard, Role
from a2a.utils.message import get_message_text
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH


class MultiAgentClient:
    """A client that can discover and interact with multiple A2A agents."""
    
    def __init__(self):
        self.agents: Dict[str, dict] = {}
        self.httpx_client = httpx.AsyncClient()
        self.client_config = ClientConfig(
            httpx_client=self.httpx_client,
            streaming=False,
        )
        self.client_factory = ClientFactory(self.client_config)
    
    async def discover_agent(self, base_url: str, agent_name: str) -> Optional[AgentCard]:
        """Discover an agent by fetching its agent card."""
        try:
            resolver = A2ACardResolver(
                httpx_client=self.httpx_client,
                base_url=base_url,
            )
            
            logging.info(f"Discovering {agent_name} at {base_url}")
            agent_card = await resolver.get_agent_card()
            
            # Create client for this agent
            client = self.client_factory.create(agent_card)
            
            # Store agent info
            self.agents[agent_name] = {
                'card': agent_card,
                'client': client,
                'base_url': base_url
            }
            
            logging.info(f"Successfully discovered {agent_name}: {agent_card.name}")
            return agent_card
            
        except Exception as e:
            logging.error(f"Failed to discover {agent_name} at {base_url}: {e}")
            return None
    
    async def discover_all_agents(self):
        """Discover all known agents."""
        agents_to_discover = [
            ("http://localhost:9999", "echo"),
            ("http://localhost:8001", "websearch"),
            ("http://localhost:8002", "calculator"),
        ]
        
        logging.info("🔍 Discovering available agents...")
        
        for base_url, agent_name in agents_to_discover:
            await self.discover_agent(base_url, agent_name)
        
        logging.info(f"✅ Discovery complete. Found {len(self.agents)} agents.")
    
    def display_agents(self):
        """Display information about discovered agents."""
        if not self.agents:
            print("❌ No agents discovered yet.")
            return
        
        print(f"\n🤖 **Discovered {len(self.agents)} A2A Agents:**\n")
        
        for agent_name, agent_info in self.agents.items():
            card = agent_info['card']
            print(f"**{card.name}** ({agent_name})")
            print(f"  📍 URL: {agent_info['base_url']}")
            print(f"  📝 Description: {card.description}")
            print(f"  🎯 Skills:")
            
            for skill in card.skills:
                print(f"    • {skill.name}: {skill.description}")
                if skill.examples:
                    print(f"      Examples: {', '.join(skill.examples[:2])}")
            
            print(f"  🔧 Capabilities: Streaming={card.capabilities.streaming}, Push Notifications={card.capabilities.push_notifications}")
            print()
    
    def suggest_agent_for_query(self, query: str) -> Optional[str]:
        """Suggest the best agent for a given query based on skills and keywords."""
        query_lower = query.lower()
        
        # Define keywords for each agent type
        agent_keywords = {
            'echo': ['echo', 'repeat', 'say back', 'test'],
            'calculator': ['calculate', 'math', 'compute', '+', '-', '*', '/', 'sqrt', 'sin', 'cos', 'pi', 'equation', 'formula'],
            'websearch': ['search', 'find', 'what is', 'who is', 'where is', 'how to', 'latest', 'news', 'information', 'lookup']
        }
        
        # Score each agent based on keyword matches
        scores = {}
        for agent_name in self.agents.keys():
            score = 0
            keywords = agent_keywords.get(agent_name, [])
            for keyword in keywords:
                if keyword in query_lower:
                    score += 1
            scores[agent_name] = score
        
        # Return agent with highest score, or None if no matches
        if not scores or max(scores.values()) == 0:
            return None
        
        return max(scores, key=scores.get)
    
    async def send_to_agent(self, agent_name: str, message: str) -> str:
        """Send a message to a specific agent and return the response."""
        if agent_name not in self.agents:
            return f"❌ Agent '{agent_name}' not found. Available agents: {list(self.agents.keys())}"
        
        try:
            agent_info = self.agents[agent_name]
            client = agent_info['client']
            card = agent_info['card']
            
            # Create message
            message_obj = create_text_message_object(
                role=Role.user,
                content=message
            )
            
            # Send message and get response
            response_text = ""
            async for event in client.send_message(message_obj):
                if isinstance(event, tuple):  # (Task, UpdateEvent)
                    task, update_event = event
                    if task.history:
                        for msg in task.history:
                            if msg.role == Role.agent:
                                response_text = get_message_text(msg)
                                break
                else:  # Direct Message
                    response_text = get_message_text(event)
            
            return response_text if response_text else "No response received"
            
        except Exception as e:
            return f"❌ Error communicating with {agent_name}: {str(e)}"
    
    async def interactive_chat(self):
        """Run an interactive chat session with agent suggestions."""
        print("\n🎉 **A2A Multi-Agent Chat Interface**")
        print("Type your questions and I'll suggest the best agent!")
        print("Commands: 'agents' (list agents), 'quit' (exit)")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'agents':
                    self.display_agents()
                    continue
                
                if not user_input:
                    continue
                
                # Suggest best agent
                suggested_agent = self.suggest_agent_for_query(user_input)
                
                if suggested_agent:
                    agent_card = self.agents[suggested_agent]['card']
                    print(f"🎯 **Suggested Agent:** {agent_card.name}")
                    print(f"📝 **Sending to:** {suggested_agent}")
                    
                    # Send to suggested agent
                    response = await self.send_to_agent(suggested_agent, user_input)
                    print(f"\n🤖 **{agent_card.name}:** {response}")
                else:
                    print("🤔 **No specific agent suggested.** Trying Echo Agent as default...")
                    response = await self.send_to_agent('echo', user_input)
                    print(f"\n🤖 **Echo Agent:** {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def run_examples(self):
        """Run example queries to demonstrate different agents."""
        examples = [
            ("Hello A2A World!", "Echo test"),
            ("What is artificial intelligence?", "Web search test"),
            ("Calculate 2 + 3 * 4", "Math calculation test"),
            ("sqrt(16) + pi", "Advanced math test"),
            ("Latest news about climate change", "Web search test"),
        ]
        
        print("\n🚀 **Running Example Queries:**\n")
        
        for query, description in examples:
            print(f"📝 **Query:** {query} ({description})")
            
            # Get suggestion
            suggested_agent = self.suggest_agent_for_query(query)
            
            if suggested_agent and suggested_agent in self.agents:
                agent_name = self.agents[suggested_agent]['card'].name
                print(f"🎯 **Suggested Agent:** {agent_name}")
                
                # Send query
                response = await self.send_to_agent(suggested_agent, query)
                print(f"🤖 **Response:** {response}")
            else:
                print("❌ No suitable agent found")
            
            print("-" * 60)
    
    async def close(self):
        """Clean up resources."""
        await self.httpx_client.aclose()


async def main():
    """Main function to run the multi-agent client."""
    logging.basicConfig(level=logging.INFO)
    
    client = MultiAgentClient()
    
    try:
        # Discover all agents
        await client.discover_all_agents()
        
        # Display discovered agents
        client.display_agents()
        
        # Run examples
        await client.run_examples()
        
        # Start interactive chat
        await client.interactive_chat()
        
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(main())