import asyncio
import uuid
from google_a2a.common.client import A2AClient
from google_a2a.common.types import AgentCard, AgentCapabilities, Message

async def main():
    try:
        agent_card = AgentCard(
        name="Orchestrator Agent",
        description="Central orchestrator agent that directs subtasks to all other agents.",
        url="http://localhost:8000",  # 👈 this is where your orchestrator is running
        version="0.1.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[]
    )
        orch = A2AClient(agent_card=agent_card)
        
        payload = {
            "id": str(uuid.uuid4()),
            "message": Message(
                role="user",
                parts=[{"type": "text", "text": "yarr"}]
            ).model_dump()
        }
        async for response in orch.send_task_streaming(payload=payload):
            print(response.status.message.parts[0].text)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
