import asyncio
import uuid
import click
from aioconsole import ainput
from google_a2a.common.client import A2AClient
from google_a2a.common.types import AgentCard, AgentCapabilities, Message


async def interact_with_agent():
    agent_card = AgentCard(
        name="Orchestrator Agent",
        description="Central orchestrator agent that directs subtasks to all other agents.",
        url="http://localhost:8000",
        version="0.1.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[],
    )
    orch = A2AClient(agent_card=agent_card)

    task_id = str(uuid.uuid4())  # ✅ persist this for the whole session
    user_input = await ainput("How can I help you today?\n> ")

    while True:
        print(f"[LOOP] Sending input: '{user_input}' with task_id {task_id}")
        payload = {
            "id": task_id,
            "message": Message(
                role="user",
                parts=[{"type": "text", "text": user_input}]
            ).model_dump()
        }

        input_required = False

        async for response in orch.send_task_streaming(payload=payload):
            state = response.result.status.state
            # print("DEBUG STATE:", state)
            for part in response.result.status.message.parts:
                print(part.text)
            if state == "input_required":
                input_required = True
            elif state == "completed":
                return

        if input_required:
            user_input = "N"
            print("FAKE RESPONDING WITH N")
            continue
        else:
            break


@click.command()
def main():
    asyncio.run(interact_with_agent())


if __name__ == "__main__":
    main()
