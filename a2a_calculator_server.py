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

from app.calculator_agent import CalculatorAgent
from app.calculator_agent_executor import CalculatorAgentExecutor


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=8002)
def main(host, port):
    """Starts the Calculator Agent server."""
    try:
        capabilities = AgentCapabilities(streaming=True, push_notifications=True)
        # Enhanced skills with detailed A2A protocol information
        skills = [
            AgentSkill(
                id='calculate',
                name='Mathematical Calculator',
                description='Performs mathematical calculations and evaluates expressions using safe evaluation through A2A protocol',
                tags=['math', 'calculation', 'arithmetic', 'algebra', 'functions', 'a2a protocol'],
                examples=[
                    '2 + 3 * 4',
                    'sqrt(16) + sin(pi/2)',
                    '2**3 + log10(100)',
                    'Calculate the area of a circle with radius 5: pi * 5**2',
                    'cos(pi) + abs(-5)'
                ],
            ),
            AgentSkill(
                id='mathematical_functions',
                name='Advanced Mathematical Functions',
                description='Supports trigonometric, logarithmic, and other mathematical functions for complex calculations',
                tags=['trigonometry', 'logarithms', 'advanced math', 'functions'],
                examples=[
                    'sin(pi/4) + cos(pi/4)',
                    'log(e) + log10(100)',
                    'sqrt(abs(-16))',
                    'floor(3.7) + ceil(3.2)'
                ],
            ),
            AgentSkill(
                id='computation_service',
                name='A2A Computation Service',
                description='Provides computational services to other A2A agents requiring mathematical operations',
                tags=['computation', 'service', 'a2a protocol', 'mathematical operations'],
                examples=[
                    'compute mathematical expressions',
                    'evaluate formulas',
                    'perform calculations for other agents'
                ],
            )
        ]
        agent_card = AgentCard(
            name='Calculator Agent',
            description='A specialized A2A agent for mathematical calculations, from basic arithmetic to complex expressions with functions. Provides computational services to the A2A ecosystem.',
            url=f'http://{host}:{port}/',
            version='1.0.0',
            default_input_modes=CalculatorAgent.SUPPORTED_CONTENT_TYPES,
            default_output_modes=CalculatorAgent.SUPPORTED_CONTENT_TYPES,
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
            agent_executor=CalculatorAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_config_store=push_config_store,
            push_sender=push_sender
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, 
            http_handler=request_handler
        )

        logger.info(f"Starting Calculator Agent server on {host}:{port}")
        uvicorn.run(server.build(), host=host, port=port)

    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()