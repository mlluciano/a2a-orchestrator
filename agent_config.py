from google_a2a.common.types import AgentSkill, AgentCapabilities, AgentCard
capabilities = AgentCapabilities(
    streaming=True
  )
skill = AgentSkill(
    id="my-project-echo-skill",
    name="Echo Tool",
    description="Echos the input given",
    tags=["echo", "repeater"],
    examples=["I will see this echoed back to me"],
    inputModes=["text"],
    outputModes=["text"],
  )
AGENT_REGISTRY = {
    "biodiversity": AgentCard(
    name="Echo Agent",
    description="This agent echos the input given",
    url="http://localhost:10002",
    version="0.1.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=capabilities,
    skills=[skill]
  )
}
