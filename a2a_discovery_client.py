"""A2A Discovery Client - Uses A2A protocol for agent discovery and interaction."""

import asyncio
import logging
from typing import Dict, List, Optional

import httpx

from a2a.client import A2ACardResolver, ClientFactory, ClientConfig
from a2a.client.helpers import create_text_message_object
from a2a.types import AgentCard, Role
from a2a.utils.message import get_message_text
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH


class A2ADiscoveryClient:
    """A client that uses A2A protocol for agent discovery and ecosystem interaction."""
    
    def __init__(self):
        self.httpx_client = httpx.AsyncClient()
        self.client_config = ClientConfig(
            httpx_client=self.httpx_client,
            streaming=False,
        )
        self.client_factory = ClientFactory(self.client_config)
        self.discovered_agents: Dict[str, dict] = {}
        self.registry_client = None
    
    async def discover_a2a_ecosystem(self):
        """Discover the A2A ecosystem starting with the registry."""
        logging.info("🔍 Starting A2A Ecosystem Discovery...")
        
        # Known A2A ecosystem endpoints
        ecosystem_agents = [
            {"name": "A2A Registry", "url": "http://localhost:8000", "role": "discovery"},
            {"name": "Echo Agent", "url": "http://localhost:9999", "role": "testing"},
            {"name": "Web Search Agent", "url": "http://localhost:8001", "role": "information"},
            {"name": "Calculator Agent", "url": "http://localhost:8002", "role": "computation"},
            {"name": "Coordinator Agent", "url": "http://localhost:8003", "role": "orchestration"},
        ]
        
        discovered_count = 0
        
        for agent_info in ecosystem_agents:
            try:
                logging.info(f"🤖 Discovering {agent_info['name']} via A2A protocol...")
                
                # Use A2A Card Resolver to get agent card
                resolver = A2ACardResolver(
                    httpx_client=self.httpx_client,
                    base_url=agent_info['url']
                )
                
                agent_card = await resolver.get_agent_card()
                client = self.client_factory.create(agent_card)
                
                # Store discovered agent with A2A details
                self.discovered_agents[agent_info['name']] = {
                    'card': agent_card,
                    'client': client,
                    'url': agent_info['url'],
                    'role': agent_info['role'],
                    'discovered_via': 'A2A Card Resolution'
                }
                
                # Special handling for registry
                if agent_info['role'] == 'discovery':
                    self.registry_client = client
                
                discovered_count += 1
                logging.info(f"✅ {agent_info['name']} discovered successfully")
                
            except Exception as e:
                logging.warning(f"⚠️  Failed to discover {agent_info['name']}: {e}")
        
        logging.info(f"🎉 A2A Discovery Complete: {discovered_count}/{len(ecosystem_agents)} agents discovered")
        return discovered_count
    
    async def query_registry_via_a2a(self, query: str) -> str:
        """Query the A2A registry using A2A protocol."""
        if not self.registry_client:
            return "❌ A2A Registry not available"
        
        try:
            # Create A2A message
            message = create_text_message_object(
                role=Role.user,
                content=query
            )
            
            # Send via A2A protocol
            response_text = ""
            async for event in self.registry_client.send_message(message):
                if isinstance(event, tuple):  # (Task, UpdateEvent)
                    task, update_event = event
                    if task.history:
                        for msg in task.history:
                            if msg.role == Role.agent:
                                response_text = get_message_text(msg)
                                break
                else:  # Direct Message
                    response_text = get_message_text(event)
            
            return response_text if response_text else "No response from registry"
            
        except Exception as e:
            return f"❌ Error querying registry: {e}"
    
    async def send_a2a_message(self, agent_name: str, message: str) -> str:
        """Send a message to an agent using A2A protocol."""
        if agent_name not in self.discovered_agents:
            return f"❌ Agent '{agent_name}' not discovered in A2A ecosystem"
        
        try:
            agent_info = self.discovered_agents[agent_name]
            client = agent_info['client']
            
            # Create A2A message
            message_obj = create_text_message_object(
                role=Role.user,
                content=message
            )
            
            # Send via A2A protocol
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
            return f"❌ A2A communication error: {e}"
    
    def display_a2a_ecosystem(self):
        """Display the discovered A2A ecosystem."""
        if not self.discovered_agents:
            print("❌ No A2A agents discovered yet.")
            return
        
        print(f"\n🌐 **A2A Ecosystem Discovery Results**")
        print(f"📊 **Discovered {len(self.discovered_agents)} A2A Agents**\n")
        
        for agent_name, agent_info in self.discovered_agents.items():
            card = agent_info['card']
            print(f"**🤖 {card.name}** ({agent_info['role']})")
            print(f"  📍 **A2A Endpoint:** {agent_info['url']}")
            print(f"  📋 **Description:** {card.description}")
            print(f"  🔗 **Protocol Version:** {getattr(card, 'protocol_version', 'N/A')}")
            print(f"  ⚙️ **Discovery Method:** {agent_info['discovered_via']}")
            
            # Show A2A capabilities
            print(f"  🔧 **A2A Capabilities:**")
            print(f"    • Streaming: {card.capabilities.streaming}")
            print(f"    • Push Notifications: {card.capabilities.push_notifications}")
            
            # Show A2A skills
            print(f"  🎯 **A2A Skills ({len(card.skills)}):**")
            for skill in card.skills[:2]:  # Show first 2 skills
                print(f"    • {skill.name}: {skill.description}")
                if skill.examples:
                    print(f"      Example: {skill.examples[0]}")
            
            if len(card.skills) > 2:
                print(f"    • ... and {len(card.skills) - 2} more skills")
            
            print()
    
    async def run_a2a_demonstration(self):
        """Run a demonstration of A2A protocol features."""
        print("\n🚀 **A2A Protocol Demonstration**\n")
        
        # Test cases showcasing A2A protocol
        a2a_test_cases = [
            {
                'title': 'A2A Registry Discovery',
                'agent': 'A2A Registry',
                'message': 'list all agents',
                'description': 'Query registry for ecosystem overview'
            },
            {
                'title': 'A2A Protocol Testing',
                'agent': 'Echo Agent',
                'message': 'Test A2A protocol communication',
                'description': 'Test basic A2A message flow'
            },
            {
                'title': 'A2A Information Retrieval',
                'agent': 'Web Search Agent',
                'message': 'What is the A2A protocol?',
                'description': 'Information lookup via A2A'
            },
            {
                'title': 'A2A Computation Service',
                'agent': 'Calculator Agent',
                'message': 'Calculate pi * 2**3',
                'description': 'Mathematical computation via A2A'
            },
            {
                'title': 'A2A Multi-Agent Coordination',
                'agent': 'Coordinator Agent',
                'message': 'Calculate 15 + 25 and search for mathematics',
                'description': 'Complex coordination via A2A'
            }
        ]
        
        for i, test_case in enumerate(a2a_test_cases, 1):
            print(f"**Test {i}: {test_case['title']}**")
            print(f"📝 Description: {test_case['description']}")
            print(f"🎯 Target Agent: {test_case['agent']}")
            print(f"💬 A2A Message: '{test_case['message']}'")
            
            # Send A2A message
            response = await self.send_a2a_message(test_case['agent'], test_case['message'])
            print(f"🤖 **A2A Response:**")
            
            # Format response nicely
            response_lines = response.split('\n')
            for line in response_lines[:5]:  # Show first 5 lines
                print(f"   {line}")
            
            if len(response_lines) > 5:
                print(f"   ... (truncated, full response has {len(response_lines)} lines)")
            
            print("\n" + "─" * 60 + "\n")
            
            # Brief pause between tests
            await asyncio.sleep(1)
    
    async def interactive_a2a_session(self):
        """Run an interactive A2A session."""
        print("\n🎮 **Interactive A2A Session**")
        print("Commands: 'agents' (show ecosystem), 'registry <query>' (query registry), 'quit' (exit)")
        print("Or send messages like: '<agent_name>: <message>'")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n💬 A2A Command: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 A2A Session Ended!")
                    break
                
                if user_input.lower() == 'agents':
                    self.display_a2a_ecosystem()
                    continue
                
                if user_input.lower().startswith('registry '):
                    query = user_input[9:]  # Remove 'registry '
                    response = await self.query_registry_via_a2a(query)
                    print(f"\n🔍 **A2A Registry Response:**\n{response}")
                    continue
                
                # Parse agent:message format
                if ':' in user_input:
                    parts = user_input.split(':', 1)
                    agent_name = parts[0].strip()
                    message = parts[1].strip()
                    
                    # Find matching agent (case insensitive)
                    matching_agent = None
                    for discovered_name in self.discovered_agents.keys():
                        if agent_name.lower() in discovered_name.lower():
                            matching_agent = discovered_name
                            break
                    
                    if matching_agent:
                        print(f"📤 Sending A2A message to {matching_agent}...")
                        response = await self.send_a2a_message(matching_agent, message)
                        print(f"\n🤖 **{matching_agent} Response:**\n{response}")
                    else:
                        print(f"❌ Agent '{agent_name}' not found. Available agents:")
                        for name in self.discovered_agents.keys():
                            print(f"  • {name}")
                else:
                    print("💡 Usage: '<agent_name>: <message>' or try 'registry list agents'")
                
            except KeyboardInterrupt:
                print("\n👋 A2A Session Ended!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def close(self):
        """Clean up resources."""
        await self.httpx_client.aclose()


async def main():
    """Main function to run the A2A discovery client."""
    logging.basicConfig(level=logging.INFO)
    
    client = A2ADiscoveryClient()
    
    try:
        # Discover A2A ecosystem
        await client.discover_a2a_ecosystem()
        
        # Display ecosystem
        client.display_a2a_ecosystem()
        
        # Run A2A demonstration
        await client.run_a2a_demonstration()
        
        # Interactive session
        await client.interactive_a2a_session()
        
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(main())