# Differences Between Documentation Examples and Actual A2A SDK

## Important Note
The A2A documentation examples you may find online often show a simplified or different API than the actual Python SDK implementation. Here are the key differences:

## Documentation Examples (Not Actual SDK)
```python
# This API doesn't exist in the actual SDK
from a2a import A2AServer, Message, TextContent, MessageRole, run_server

class EchoAgent(A2AServer):
    def handle_message(self, message):
        if message.content.type == "text":
            return Message(
                content=TextContent(text=f"Echo: {message.content.text}"),
                role=MessageRole.AGENT
            )

run_server(agent, host="0.0.0.0", port=9999)
```

## Actual A2A SDK Implementation
```python
# This is the real SDK structure
from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.apps.jsonrpc.starlette_app import A2AStarletteApplication
from a2a.utils.message import get_message_text, new_agent_text_message

class EchoAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue):
        input_text = get_message_text(context.message)
        echo_text = f"Echo: {input_text}"
        
        response_message = new_agent_text_message(
            text=echo_text,
            context_id=context.message.context_id,
            task_id=context.task_id,
        )
        
        task_status = TaskStatus(state=TaskState.completed)
        task = Task(
            id=context.task_id,
            context_id=context.message.context_id,
            status=task_status,
            history=[context.message, response_message],
        )
        
        await event_queue.enqueue_event(task)
```

## Key Differences

| Documentation Examples | Actual SDK Implementation |
|------------------------|---------------------------|
| `A2AServer` class | `AgentExecutor` pattern |
| `TextContent` | `Part.root` with `TextPart` |
| `message.content.text` | `get_message_text(message)` |
| `run_server()` function | `A2AStarletteApplication` + `uvicorn` |
| `publish()` method | `enqueue_event()` method |
| `state` field in Task | `status` field with `TaskStatus` |
| `A2AClient` (simple) | `ClientFactory` pattern |

## Why This Happens
- Documentation examples are often simplified for clarity
- The actual SDK provides more structure and flexibility
- The SDK follows enterprise-grade patterns (factories, dependency injection, etc.)
- Some examples may be from older versions or different implementations

## What We Built
Our implementation uses the **actual SDK structure** and follows the correct patterns:
- ✅ `AgentExecutor` for agent logic
- ✅ `EventQueue.enqueue_event()` for publishing events
- ✅ `Part.root` for accessing message content
- ✅ `ClientFactory` for creating clients
- ✅ Proper `Task` and `TaskStatus` structures
- ✅ Utility functions like `get_message_text()`

This ensures compatibility with the real A2A Python SDK and follows best practices.