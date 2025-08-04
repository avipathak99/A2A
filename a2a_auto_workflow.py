"""A2A Automatic Workflow Demonstration - Shows agents working together automatically."""

import asyncio
import logging

from app.auto_workflow_manager import AutoWorkflowManager
from app.intelligent_router import IntelligentA2ARouter


async def demonstrate_automatic_workflows():
    """Demonstrate how A2A agents work together automatically."""
    
    print("🤖 **A2A Automatic Agent Workflows**")
    print("=" * 60)
    print("This demonstrates how A2A agents automatically:")
    print("• Discover each other in the ecosystem")
    print("• Route queries to appropriate agents")
    print("• Execute complex multi-agent workflows")
    print("• Coordinate tasks without manual intervention")
    print("=" * 60)
    
    workflow_manager = AutoWorkflowManager()
    
    try:
        # Initialize automatic system
        print("\n🔄 **Initializing Automatic A2A System...**")
        await workflow_manager.initialize()
        
        # Show available workflows
        print("\n" + workflow_manager.list_workflows())
        
        # Demo 1: Single automatic workflow
        print("🎯 **Demo 1: Automatic Research & Calculate Workflow**")
        results = await workflow_manager.execute_workflow('research_calculate')
        
        # Demo 2: Complex problem solving workflow
        print("\n🎯 **Demo 2: Automatic Problem Solving Workflow**")
        results = await workflow_manager.execute_workflow('problem_solving')
        
        # Demo 3: Dynamic workflow creation
        print("\n🎯 **Demo 3: Dynamic Workflow Creation**")
        dynamic_description = "Find information about machine learning and calculate some related statistics"
        await workflow_manager.create_dynamic_workflow(dynamic_description)
        
        # Demo 4: Interactive automatic mode
        await interactive_automatic_workflows(workflow_manager)
        
    except Exception as e:
        print(f"❌ Error in workflow demonstration: {e}")
    finally:
        await workflow_manager.cleanup()


async def interactive_automatic_workflows(workflow_manager: AutoWorkflowManager):
    """Interactive mode for automatic workflows."""
    
    print("\n🎮 **Interactive Automatic Workflows**")
    print("Commands:")
    print("• 'list' - Show available workflows")
    print("• 'run <workflow_name>' - Execute a specific workflow")
    print("• 'all' - Run all workflows")
    print("• 'create <description>' - Create dynamic workflow")
    print("• 'quit' - Exit")
    print("-" * 50)
    
    while True:
        try:
            command = input("\n🤖 Workflow Command: ").strip()
            
            if command.lower() in ['quit', 'exit']:
                print("👋 Automatic workflow mode ended!")
                break
            
            if command.lower() == 'list':
                print(workflow_manager.list_workflows())
                continue
            
            if command.lower() == 'all':
                print("🚀 **Running All Automatic Workflows...**")
                await workflow_manager.run_all_workflows()
                continue
            
            if command.lower().startswith('run '):
                workflow_name = command[4:].strip()
                try:
                    await workflow_manager.execute_workflow(workflow_name)
                except ValueError as e:
                    print(f"❌ {e}")
                    print("Available workflows:", list(workflow_manager.workflows.keys()))
                continue
            
            if command.lower().startswith('create '):
                description = command[7:].strip()
                if description:
                    await workflow_manager.create_dynamic_workflow(description)
                else:
                    print("❌ Please provide a description for the workflow")
                continue
            
            if not command:
                continue
            
            print("❌ Unknown command. Type 'quit' to exit or 'list' to see workflows.")
            
        except KeyboardInterrupt:
            print("\n👋 Automatic workflow mode ended!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


async def showcase_automatic_intelligence():
    """Showcase the automatic intelligence of A2A agents."""
    
    print("\n🧠 **A2A Automatic Intelligence Showcase**")
    print("=" * 50)
    
    router = IntelligentA2ARouter()
    
    try:
        await router.auto_discover_ecosystem()
        
        # Test automatic routing intelligence
        intelligent_test_cases = [
            {
                'query': 'Hello world',
                'expected': 'Should automatically route to Echo Agent for testing'
            },
            {
                'query': 'Calculate the square root of 144',
                'expected': 'Should automatically route to Calculator Agent for math'
            },
            {
                'query': 'What is the capital of France?',
                'expected': 'Should automatically route to Web Search Agent for information'
            },
            {
                'query': 'Find agents that can do calculations',
                'expected': 'Should automatically route to Registry Agent for discovery'
            },
            {
                'query': 'Calculate 2+3 and search for mathematics history',
                'expected': 'Should automatically route to Coordinator Agent for multi-step tasks'
            },
            {
                'query': 'Some random query that doesnt match patterns',
                'expected': 'Should fallback to Echo Agent as default'
            }
        ]
        
        print("🔍 **Testing Automatic Routing Intelligence:**\n")
        
        for i, test_case in enumerate(intelligent_test_cases, 1):
            query = test_case['query']
            expected = test_case['expected']
            
            print(f"**Test {i}:** {query}")
            print(f"📝 Expected: {expected}")
            
            # Get automatic routing decision
            agent_type, agent_name, routing_reason = await router.auto_route_query(query)
            print(f"🎯 **Auto-Decision:** Route to {agent_name}")
            print(f"🧠 **Reasoning:** {routing_reason}")
            
            # Execute automatically
            response = await router.auto_execute_query(query)
            print(f"🤖 **Auto-Response:** {response[:100]}{'...' if len(response) > 100 else ''}")
            print("-" * 40)
        
        print("✅ **Automatic Intelligence Test Complete!**")
        
    finally:
        await router.cleanup()


async def main():
    """Main function for automatic workflow demonstrations."""
    
    logging.basicConfig(level=logging.WARNING)  # Reduce log noise
    
    print("🚀 **A2A Automatic Agent System**\n")
    print("This system demonstrates how A2A agents can work together")
    print("automatically without manual intervention.\n")
    
    print("Choose demonstration:")
    print("1. 🔄 Full automatic workflow demonstration")
    print("2. 🧠 Automatic intelligence showcase")
    print("3. 🎮 Interactive automatic mode")
    print("4. 🚀 All demonstrations")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            await demonstrate_automatic_workflows()
        elif choice == "2":
            await showcase_automatic_intelligence()
        elif choice == "3":
            workflow_manager = AutoWorkflowManager()
            try:
                await workflow_manager.initialize()
                await interactive_automatic_workflows(workflow_manager)
            finally:
                await workflow_manager.cleanup()
        elif choice == "4":
            await showcase_automatic_intelligence()
            await demonstrate_automatic_workflows()
        else:
            print("Invalid choice, running full demonstration...")
            await demonstrate_automatic_workflows()
            
    except KeyboardInterrupt:
        print("\n👋 Thanks for exploring A2A automatic systems!")


if __name__ == '__main__':
    asyncio.run(main())