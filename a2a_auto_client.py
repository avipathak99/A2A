"""A2A Automatic Client - Demonstrates automatic agent discovery and routing."""

import asyncio
import logging

from app.intelligent_router import IntelligentA2ARouter


async def demonstrate_automatic_usage():
    """Demonstrate automatic A2A agent usage."""
    
    router = IntelligentA2ARouter()
    
    try:
        print("🌐 **A2A Automatic Agent Usage Demonstration**\n")
        
        # Step 1: Auto-discover ecosystem
        print("=" * 60)
        print("**STEP 1: Automatic A2A Ecosystem Discovery**")
        print("=" * 60)
        
        await router.auto_discover_ecosystem()
        
        # Step 2: Show routing capabilities
        print("\n" + "=" * 60)
        print("**STEP 2: Automatic Routing Capabilities**")
        print("=" * 60)
        
        print(router.get_routing_summary())
        
        # Step 3: Automatic query processing
        print("\n" + "=" * 60)
        print("**STEP 3: Automatic Query Processing**")
        print("=" * 60)
        
        # Test queries that demonstrate automatic routing
        test_queries = [
            "Hello, are you working?",  # Should route to Echo Agent
            "Calculate 15 * 23 + sqrt(144)",  # Should route to Calculator Agent
            "What is artificial intelligence?",  # Should route to Web Search Agent
            "Find agents that can do math",  # Should route to Registry Agent
            "Calculate pi * 2 and search for mathematics",  # Should route to Coordinator Agent
        ]
        
        print("🎯 **Automatic routing and execution of diverse queries:**\n")
        
        results = await router.batch_auto_process(test_queries)
        
        # Step 4: Show results summary
        print("=" * 60)
        print("**STEP 4: Automatic Processing Results**")
        print("=" * 60)
        
        for result in results:
            print(f"**Query:** {result['query']}")
            print(f"**Auto-Response:** {result['response'][:200]}{'...' if len(result['response']) > 200 else ''}")
            print("-" * 40)
        
        # Step 5: Interactive automatic mode
        print("\n" + "=" * 60)
        print("**STEP 5: Interactive Automatic Mode**")
        print("=" * 60)
        
        await interactive_automatic_mode(router)
        
    except Exception as e:
        print(f"❌ Error in demonstration: {e}")
    finally:
        await router.cleanup()


async def interactive_automatic_mode(router: IntelligentA2ARouter):
    """Interactive mode where all queries are automatically routed."""
    
    print("\n🎮 **Interactive Automatic A2A Mode**")
    print("Just type your query - the system will automatically:")
    print("• Determine the best agent for your query")
    print("• Route your message via A2A protocol")
    print("• Return the response from the appropriate agent")
    print("\nCommands: 'routing' (show routing info), 'quit' (exit)")
    print("-" * 50)
    
    while True:
        try:
            query = input("\n🤖 Auto-Query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'bye']:
                print("👋 Automatic A2A mode ended!")
                break
            
            if query.lower() == 'routing':
                print(router.get_routing_summary())
                continue
            
            if not query:
                continue
            
            # Automatic processing
            print("🔄 **Auto-processing...**")
            response = await router.auto_execute_query(query)
            print(f"🤖 **Auto-Response:**\n{response}")
            
        except KeyboardInterrupt:
            print("\n👋 Automatic A2A mode ended!")
            break
        except Exception as e:
            print(f"❌ Auto-processing error: {e}")


async def run_automatic_workflow_examples():
    """Run examples of automatic workflows."""
    
    router = IntelligentA2ARouter()
    
    try:
        # Discover ecosystem
        await router.auto_discover_ecosystem()
        
        print("\n🔄 **Automatic Workflow Examples**\n")
        
        # Example 1: Automatic mathematical workflow
        print("**Example 1: Automatic Mathematical Workflow**")
        math_queries = [
            "Calculate the area of circle with radius 5",
            "What is the value of pi?",
            "Compute 2^8 + sqrt(64)",
        ]
        
        for query in math_queries:
            response = await router.auto_execute_query(query)
            print(f"   Query: {query}")
            print(f"   Auto-Response: {response[:100]}...\n")
        
        # Example 2: Automatic information retrieval workflow
        print("**Example 2: Automatic Information Retrieval Workflow**")
        info_queries = [
            "What is machine learning?",
            "Latest news about climate change",
            "How does quantum computing work?",
        ]
        
        for query in info_queries:
            response = await router.auto_execute_query(query)
            print(f"   Query: {query}")
            print(f"   Auto-Response: {response[:100]}...\n")
        
        # Example 3: Automatic ecosystem management
        print("**Example 3: Automatic Ecosystem Management**")
        mgmt_queries = [
            "List all available agents",
            "Find agents that can calculate",
            "Show me web search capabilities",
        ]
        
        for query in mgmt_queries:
            response = await router.auto_execute_query(query)
            print(f"   Query: {query}")
            print(f"   Auto-Response: {response[:100]}...\n")
    
    finally:
        await router.cleanup()


async def main():
    """Main function with different demonstration modes."""
    
    logging.basicConfig(level=logging.WARNING)  # Reduce noise
    
    print("🚀 **A2A Automatic Agent Usage**\n")
    print("Choose demonstration mode:")
    print("1. Full demonstration (recommended)")
    print("2. Interactive automatic mode only")
    print("3. Workflow examples only")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            await demonstrate_automatic_usage()
        elif choice == "2":
            router = IntelligentA2ARouter()
            try:
                await router.auto_discover_ecosystem()
                await interactive_automatic_mode(router)
            finally:
                await router.cleanup()
        elif choice == "3":
            await run_automatic_workflow_examples()
        else:
            print("Invalid choice, running full demonstration...")
            await demonstrate_automatic_usage()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == '__main__':
    asyncio.run(main())