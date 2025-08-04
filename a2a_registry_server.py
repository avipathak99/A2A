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

from app.agent_registry import AgentRegistry
from app.agent_registry_executor import AgentRegistryExecutor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=8000)
def main(host, port):
    """Starts the A2A Agent Registry server."""
    try:
        capabilities = AgentCapabilities(streaming=True, push_notifications=True)
        
        # Define skills for the registry
        registry_skills = [
            AgentSkill(
                id='agent_discovery',
                name='Agent Discovery',
                description='Discover and search for A2A agents in the ecosystem',
                tags=['discovery', 'search', 'registry', 'a2a protocol'],
                examples=[
                    'list all agents',
                    'search for calculator agents',
                    'find agents that can do web search',
                    'show me available agents'
                ],
            ),
            AgentSkill(
                id='agent_information',
                name='Agent Information',
                description='Get detailed information about specific A2A agents',
                tags=['information', 'details', 'agent cards', 'capabilities'],
                examples=[
                    'details calculator_agent',
                    'info about echo_agent',
                    'show websearch_agent capabilities'
                ],
            ),
            AgentSkill(
                id='ecosystem_management',
                name='A2A Ecosystem Management',
                description='Manage and coordinate the A2A agent ecosystem',
                tags=['ecosystem', 'coordination', 'management', 'a2a protocol'],
                examples=[
                    'help',
                    'what can you do?',
                    'how does A2A work?'
                ],
            )
        ]
        
        agent_card = AgentCard(
            name='A2A Agent Registry',
            description='Central directory service for A2A agent discovery and ecosystem management. I help you find and connect with the right agents in the A2A ecosystem.',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=AgentRegistry.SUPPORTED_CONTENT_TYPES,
            default_output_modes=AgentRegistry.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=registry_skills,
        )

        # Set up the server components
        httpx_client = httpx.AsyncClient()
        push_config_store = InMemoryPushNotificationConfigStore()
        push_sender = BasePushNotificationSender(
            httpx_client=httpx_client,
            config_store=push_config_store
        )
        request_handler = DefaultRequestHandler(
            agent_executor=AgentRegistryExecutor(),
            task_store=InMemoryTaskStore(),
            push_config_store=push_config_store,
            push_sender=push_sender
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, 
            http_handler=request_handler
        )

        logger.info(f"Starting A2A Agent Registry server on {host}:{port}")
        logger.info("🔍 Registry will coordinate agent discovery and ecosystem management")
        logger.info("🤖 Agents can register and be discovered through A2A protocol")
        uvicorn.run(server.build(), host=host, port=port)

    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()