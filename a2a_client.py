"""A2A Echo Client Example."""

import asyncio
import logging
from uuid import uuid4

import httpx

from a2a.client import A2ACardResolver, ClientFactory, ClientConfig
from a2a.client.helpers import create_text_message_object
from a2a.types import Role
from a2a.utils.message import get_message_text
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH


async def main() -> None:
    """Main client function to send messages to the Echo Agent."""
    # Configure logging to show INFO level messages
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    base_url = 'http://localhost:9999'

    async with httpx.AsyncClient() as httpx_client:
        # Initialize A2ACardResolver
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url,
        )

        # Fetch Agent Card
        try:
            logger.info(f'Fetching agent card from: {base_url}{AGENT_CARD_WELL_KNOWN_PATH}')
            agent_card = await resolver.get_agent_card()
            logger.info('Successfully fetched agent card:')
            logger.info(agent_card.model_dump_json(indent=2, exclude_none=True))

        except Exception as e:
            logger.error(f'Failed to fetch agent card: {e}', exc_info=True)
            raise RuntimeError('Failed to fetch the agent card. Cannot continue.') from e

        # Initialize Client using ClientFactory
        config = ClientConfig(
            httpx_client=httpx_client,
            streaming=False,  # Use non-streaming for simplicity
        )
        factory = ClientFactory(config)
        client = factory.create(agent_card)
        logger.info('A2A Client initialized using ClientFactory.')

        # Create and send first message
        logger.info("Sending message to Echo Agent...")
        message = create_text_message_object(
            role=Role.user, 
            content="Hello A2A World!"
        )
        
        async for event in client.send_message(message):
            if isinstance(event, tuple):  # (Task, UpdateEvent)
                task, update_event = event
                logger.info("Received task response:")
                print(f"Task ID: {task.id}")
                print(f"Status: {task.status.state}")
                if task.history:
                    for msg in task.history:
                        message_text = get_message_text(msg)
                        if msg.role == Role.agent:
                            print(f"Agent response: {message_text}")
                        else:
                            print(f"User message: {message_text}")
            else:  # Direct Message
                logger.info("Received message response:")
                message_text = get_message_text(event)
                print(f"Message: {message_text}")

        # Example of multiple messages
        print("\nSending another message...")
        message2 = create_text_message_object(
            role=Role.user, 
            content="This is a test message!"
        )
        
        async for event in client.send_message(message2):
            if isinstance(event, tuple):  # (Task, UpdateEvent)
                task, update_event = event
                logger.info("Received second task response:")
                print(f"Task ID: {task.id}")
                print(f"Status: {task.status.state}")
                if task.history:
                    for msg in task.history:
                        message_text = get_message_text(msg)
                        if msg.role == Role.agent:
                            print(f"Agent response: {message_text}")
                        else:
                            print(f"User message: {message_text}")
            else:  # Direct Message
                logger.info("Received second message response:")
                message_text = get_message_text(event)
                print(f"Message: {message_text}")


if __name__ == '__main__':
    asyncio.run(main())
