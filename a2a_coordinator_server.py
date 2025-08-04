import logging
import os
import sys

import click
import httpx
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import (
    BasePushNotificationSender,
    InMemoryPushNotificationConfigStore,
    InMemoryTaskStore,
)
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from app.coordinator_agent import CoordinatorAgent
from app.coordinator_agent_executor import CoordinatorAgentExecutor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=8003)
def main(host, port):
    """Starts the A2A Coordinator Agent server."""
    try:
        capabilities = AgentCapabilities(streaming=True, push_notifications=True)
        
        # Enhanced skills showcasing A2A agent-to-agent communication
        skills = [
            AgentSkill(
                id='agent_coordination',
                name='A2A Agent Coordination',
                description='Coordinates multiple A2A agents to fulfill complex requests using the A2A protocol',
                tags=['coordination', 'multi-agent', 'a2a protocol', 'orchestration'],
                examples=[
                    'Calculate 2+3 and search for mathematics',
                    'What is quantum computing and compute pi * 2',
                    'Find agents that can help with calculations',
                    'Coordinate search and computation tasks'
                ],
            ),
            AgentSkill(
                id='a2a_communication',
                name='A2A Inter-Agent Communication',
                description='Demonstrates agent-to-agent communication using A2A protocol message passing',
                tags=['a2a protocol', 'communication', 'inter-agent', 'messaging'],
                examples=[
                    'Send calculation request to calculator agent',
                    'Query web search agent for information',
                    'Request agent list from registry',
                    'Echo test via echo agent'
                ],
            ),
            AgentSkill(
                id='complex_task_handling',
                name='Complex Task Decomposition',
                description='Breaks down complex tasks and routes sub-tasks to appropriate specialized A2A agents',
                tags=['task decomposition', 'routing', 'specialization', 'workflow'],
                examples=[
                    'Research and calculate compound tasks',
                    'Multi-step problem solving',
                    'Cross-agent workflow execution'
                ],
            )
        ]
        
        agent_card = AgentCard(
            name='A2A Coordinator Agent',
            description='A meta-agent that demonstrates the power of A2A protocol by coordinating multiple specialized agents. Showcases agent discovery, inter-agent communication, and complex task orchestration.',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=CoordinatorAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=CoordinatorAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=skills,
        )

        # Set up the server components
        httpx_client = httpx.AsyncClient()
        push_config_store = InMemoryPushNotificationConfigStore()
        push_sender = BasePushNotificationSender(
            httpx_client=httpx_client,
            config_store=push_config_store
        )
        request_handler = DefaultRequestHandler(
            agent_executor=CoordinatorAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_config_store=push_config_store,
            push_sender=push_sender
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, 
            http_handler=request_handler
        )

        logger.info(f"Starting A2A Coordinator Agent server on {host}:{port}")
        logger.info("🤝 Coordinator will demonstrate A2A agent-to-agent communication")
        logger.info("🔗 Will connect to other A2A agents in the ecosystem")
        uvicorn.run(server.build(), host=host, port=port)

    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()