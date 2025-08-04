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

from app.websearch_agent import WebSearchAgent
from app.websearch_agent_executor import WebSearchAgentExecutor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=8001)
def main(host, port):
    """Starts the Web Search Agent server."""
    try:
        capabilities = AgentCapabilities(streaming=True, push_notifications=True)
        # Enhanced skills with detailed A2A protocol information
        skills = [
            AgentSkill(
                id='web_search',
                name='Web Search',
                description='Searches the web for information using DuckDuckGo API and returns formatted results through A2A protocol',
                tags=['web search', 'information retrieval', 'research', 'lookup', 'a2a protocol'],
                examples=[
                    'What is artificial intelligence?',
                    'Latest news about climate change',
                    'Python programming tutorial',
                    'Define quantum computing',
                    'How does blockchain work?'
                ],
            ),
            AgentSkill(
                id='information_retrieval',
                name='Information Retrieval',
                description='Retrieves and formats web-based information for other A2A agents and clients',
                tags=['information', 'research', 'knowledge', 'facts', 'data'],
                examples=[
                    'Find information about machine learning',
                    'Research renewable energy trends',
                    'Look up current technology news'
                ],
            )
        ]
        agent_card = AgentCard(
            name='Web Search Agent',
            description='A specialized A2A agent that searches the web for information using DuckDuckGo API. Provides real-time information retrieval and research capabilities to the A2A ecosystem.',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=WebSearchAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=WebSearchAgent.SUPPORTED_CONTENT_TYPES,
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
            agent_executor=WebSearchAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_config_store=push_config_store,
            push_sender=push_sender
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, 
            http_handler=request_handler
        )

        logger.info(f"Starting Web Search Agent server on {host}:{port}")
        uvicorn.run(server.build(), host=host, port=port)

    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()