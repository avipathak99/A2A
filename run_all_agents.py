"""Script to start all A2A agents in separate processes for easy testing."""

import subprocess
import sys
import time
import signal
import os
from typing import List


class AgentManager:
    """Manages multiple A2A agent processes."""
    
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.agents = [
            {"name": "A2A Registry", "script": "a2a_registry_server.py", "port": 8000},
            {"name": "Echo Agent", "script": "a2a_server.py", "port": 9999},
            {"name": "Web Search Agent", "script": "a2a_websearch_server.py", "port": 8001}, 
            {"name": "Calculator Agent", "script": "a2a_calculator_server.py", "port": 8002},
            {"name": "Coordinator Agent", "script": "a2a_coordinator_server.py", "port": 8003},
        ]
    
    def start_agents(self):
        """Start all agent servers."""
        print("🚀 Starting A2A Multi-Agent System...")
        print("=" * 50)
        
        for agent in self.agents:
            try:
                print(f"Starting {agent['name']} on port {agent['port']}...")
                
                # Start agent process
                process = subprocess.Popen([
                    sys.executable, agent['script'],
                    '--host', 'localhost',
                    '--port', str(agent['port'])
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                self.processes.append(process)
                print(f"✅ {agent['name']} started (PID: {process.pid})")
                
                # Brief pause between starts
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Failed to start {agent['name']}: {e}")
        
        print("\n🎉 All agents started! Waiting for them to initialize...")
        time.sleep(3)  # Give agents time to start up
        
        print("\n📋 **Agent Summary:**")
        for agent in self.agents:
            print(f"  • {agent['name']}: http://localhost:{agent['port']}")
        
        print(f"\n🔗 **Agent Cards:**")
        for agent in self.agents:
            print(f"  • {agent['name']}: http://localhost:{agent['port']}/.well-known/agent-card.json")
    
    def stop_agents(self):
        """Stop all agent processes."""
        print("\n🛑 Stopping all agents...")
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ Agent stopped (PID: {process.pid})")
            except subprocess.TimeoutExpired:
                print(f"⚠️  Force killing agent (PID: {process.pid})")
                process.kill()
            except Exception as e:
                print(f"❌ Error stopping agent: {e}")
        
        self.processes.clear()
        print("🏁 All agents stopped.")
    
    def run_interactive(self):
        """Run agents and wait for user input to stop."""
        try:
            self.start_agents()
            
            print("\n" + "=" * 50)
            print("🎮 **Ready for Testing!**")
            print("\n📝 **Next Steps - Choose Your Experience:**")
            print("1. 🤖 **AUTOMATIC** - Agents work together automatically:")
            print("   python a2a_auto_client.py")
            print("   python a2a_auto_workflow.py")
            print("2. 🌐 **DISCOVERY** - Explore the A2A ecosystem:")
            print("   python a2a_discovery_client.py")
            print("3. 🤝 **INTERACTIVE** - Manual multi-agent client:")
            print("   python a2a_multi_client.py")
            print("4. 📢 **SIMPLE** - Basic echo test:")
            print("   python a2a_client.py")
            print("5. Press Ctrl+C here to stop all agents")
            print("\n🔍 **A2A Agent Cards:**")
            for agent in self.agents:
                print(f"   • {agent['name']}: http://localhost:{agent['port']}/.well-known/agent-card.json")
            print("=" * 50)
            
            # Wait for interrupt
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🔄 Received stop signal...")
        finally:
            self.stop_agents()


def main():
    """Main function."""
    manager = AgentManager()
    
    # Handle signals for clean shutdown
    def signal_handler(signum, frame):
        print(f"\n📡 Received signal {signum}")
        manager.stop_agents()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the manager
    manager.run_interactive()


if __name__ == '__main__':
    main()