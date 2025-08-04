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

from app.agent import EchoAgent
from app.agent_executor import EchoAgentExecutor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=9999)
def main(host, port):
    """Starts the Echo Agent server."""
    try:
        capabilities = AgentCapabilities(streaming=True, push_notifications=True)
        # Enhanced skills with detailed A2A protocol information
        skills = [
            AgentSkill(
                id='echo_skill',
                name='Echo Skill',
                description='Echoes back any text with a prefix for testing A2A communication and message flow',
                tags=['echo', 'text processing', 'testing', 'a2a protocol', 'communication'],
                examples=[
                    'Hello World -> Echo: Hello World',
                    'Test A2A message -> Echo: Test A2A message',
                    'Echo this please -> Echo: Echo this please'
                ],
            ),
            AgentSkill(
                id='a2a_testing',
                name='A2A Protocol Testing',
                description='Provides a simple endpoint for testing A2A protocol communication, message structure, and response handling',
                tags=['testing', 'a2a protocol', 'debugging', 'validation'],
                examples=[
                    'test a2a connection',
                    'validate message format',
                    'check protocol compliance'
                ],
            )
        ]
        agent_card = AgentCard(
            name='Echo Agent',
            description='A foundational A2A agent that echoes back messages with a prefix. Perfect for testing A2A protocol communication, message flow, and agent connectivity in the ecosystem.',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=EchoAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=EchoAgent.SUPPORTED_CONTENT_TYPES,
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
            agent_executor=EchoAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_config_store=push_config_store,
            push_sender=push_sender
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, 
            http_handler=request_handler
        )

        logger.info(f"Starting Echo Agent server on {host}:{port}")
        uvicorn.run(server.build(), host=host, port=port)

    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
