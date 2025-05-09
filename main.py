import logging
import click

from google_a2a.common.types import (
    AgentSkill,
    AgentCapabilities,
    AgentCard,
)
from google_a2a.common.server import A2AServer
from orchestrator import OrchestratorTaskManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--host", default="localhost")
@click.option("--port", default=8000)
def main(host, port):
    skill = AgentSkill(
        id="orchestrator-skill",
        name="Multi-Agent Orchestrator",
        description="Routes biodiversity questions to the correct agents",
        tags=["biodiversity", "routing"],
        examples=["What species live in Florida?"],
        inputModes=["text"],
        outputModes=["text"],
    )

    capabilities = AgentCapabilities(streaming=False)
    agent_card = AgentCard(
        name="Orchestrator Agent",
        description="Routes questions to appropriate domain agents",
        url=f"http://{host}:{port}/",
        version="0.1.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=capabilities,
        skills=[skill],
    )

    task_manager = OrchestratorTaskManager()
    server = A2AServer(agent_card=agent_card, task_manager=task_manager, host=host, port=port)
    server.start()


if __name__ == "__main__":
    main()
