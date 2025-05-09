from google_a2a.common.server.task_manager import InMemoryTaskManager
from google_a2a.common.types import (
    SendTaskRequest,
    SendTaskResponse,
    Message,
    TaskStatus,
    TaskState,
    Artifact,
    SendTaskStreamingRequest,
    SendTaskStreamingResponse,
    JSONRPCResponse
)
from collections.abc import AsyncIterable
from google_a2a.common.client import A2AClient
from agent_config import AGENT_REGISTRY
import uuid

class OrchestratorTaskManager(InMemoryTaskManager):
    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        await self.upsert_task(request.params)
        task_id = request.params.id
        input_text = request.params.message.parts[0].text

        # 🧠 Decide which agent to forward to
        agent_key = self.route_to_agent(input_text)
        agent_card = AGENT_REGISTRY[agent_key]
        client = A2AClient(agent_card=agent_card)

        
        payload = {
            "id": str(uuid.uuid4()),
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": "biodiversity"}]
            }
        }
        response = await client.send_task(payload=payload)

        # 📨 Grab the response and build our task result
        output_text = response.result.status.message.parts[0].text

        task = await self._update_task(task_id, TaskState.COMPLETED, output_text)
        return SendTaskResponse(id=request.id, result=task)
    
    async def on_send_task_subscribe(
        self,
        request: SendTaskStreamingRequest
    ) -> AsyncIterable[SendTaskStreamingResponse] | JSONRPCResponse:
        await self.upsert_task(request.params)
        task_id = request.params.id
        input_text = request.params.message.parts[0].text

        # Route to the correct agent
        agent_key = self.route_to_agent(input_text)
        agent_card = AGENT_REGISTRY[agent_key]
        client = A2AClient(agent_card=agent_card)

        # Collect all responses into a list and return (non-streaming workaround)
        results = []
        async for response in client.send_task_streaming(payload=request.params.model_dump()):
            print(response)
            results.append(response)
        return JSONRPCResponse(id=request.id, result=results)

    def route_to_agent(self, text: str) -> str:
        if "biodiversity" in text or "taxonomy" in text:
            return "biodiversity"
        elif "weather" in text:
            return "climate"
        else:
            return "biodiversity"  # default

    async def _update_task(self, task_id: str, state: TaskState, response_text: str):
        task = self.tasks[task_id]
        parts = [{"type": "text", "text": response_text}]
        task.status = TaskStatus(
            state=state,
            message=Message(role="agent", parts=parts)
        )
        task.artifacts = [Artifact(parts=parts)]
        return task
