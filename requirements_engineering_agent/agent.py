import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from requirements_engineering_agent.instructions import (
    INTERVIEW_AGENT_INSTRUCTION,
    ORCHESTRATOR_INSTRUCTION,
    REFACTOR_INSTRUCTION,
    REQUIREMENTS_GENERATION_INSTRUCTION,
    STAKEHOLDER_SIMULATION_INSTRUCTION,
)

load_dotenv()

if azure_token := os.getenv("AZURE_OPENAI_AD_TOKEN"):
    os.environ.setdefault("AZURE_AD_TOKEN", azure_token)

MODEL_NAME = os.getenv("AGENT4RE_MODEL", "azure/gpt-4o")
MODEL = LiteLlm(model=MODEL_NAME)

REFINED_REQUIREMENTS_GENERATION_INSTRUCTION = f"""
{REQUIREMENTS_GENERATION_INSTRUCTION}

This is a refinement round. Use the existing specification in
["generated_requirements"] and apply every relevant recommendation in
["refactoring_commands"]. Return the complete revised specification, not a
change summary or a partial document.
"""

def exit_loop(tool_context: ToolContext) -> dict:
    """End elicitation when the interviewer has enough information."""
    tool_context.actions.escalate = True
    return {}


interview_agent = LlmAgent(
    name="InterviewAgent",
    model=MODEL,
    description="Interviews a simulated stakeholder to elicit software requirements.",
    instruction=INTERVIEW_AGENT_INSTRUCTION,
    tools=[exit_loop],
    output_key="requirement_elicitation_report",
    generate_content_config=types.GenerateContentConfig(temperature=1.0),
)

stakeholder_agent = LlmAgent(
    name="StakeholderAgent",
    model=MODEL,
    description="Simulates a key stakeholder for the software project.",
    instruction=STAKEHOLDER_SIMULATION_INSTRUCTION,
    output_key="stakeholder_responses",
    generate_content_config=types.GenerateContentConfig(temperature=1.0),
)

requirement_elicitation_agent = LoopAgent(
    name="RequirementsElicitationAgent",
    description="Runs iterative requirements elicitation.",
    sub_agents=[stakeholder_agent, interview_agent],
    max_iterations=10,
)

requirement_generation_agent = LlmAgent(
    name="RequirementsGenerationAgent",
    model=MODEL,
    description="Generates an IEEE-style software requirements specification.",
    instruction=REQUIREMENTS_GENERATION_INSTRUCTION,
    output_key="generated_requirements",
    generate_content_config=types.GenerateContentConfig(temperature=0.8),
)

refactoring_agent = LlmAgent(
    name="RefactoringAgent",
    model=MODEL,
    description="Turns feedback into concrete specification improvements.",
    instruction=REFACTOR_INSTRUCTION,
    output_key="refactoring_commands",
    generate_content_config=types.GenerateContentConfig(temperature=0.2),
)

requirement_generation_agent_loop2 = LlmAgent(
    name="SecondRoundRequirementsGenerationAgent",
    model=MODEL,
    description="Regenerates the specification using the refactoring guidance.",
    instruction=REFINED_REQUIREMENTS_GENERATION_INSTRUCTION,
    output_key="generated_requirements_loop_2",
    generate_content_config=types.GenerateContentConfig(temperature=0.8),
)

sequential_agent_loop1 = SequentialAgent(
    name="SequentialAgentLoop1",
    sub_agents=[requirement_elicitation_agent, requirement_generation_agent],
)

sequential_agent_loop2 = SequentialAgent(
    name="SequentialAgentLoop2",
    sub_agents=[refactoring_agent, requirement_generation_agent_loop2],
)

orchestrator_agent = LlmAgent(
    name="OrchestratorAgent",
    model=MODEL,
    description="Coordinates the end-to-end requirements engineering workflow.",
    instruction=ORCHESTRATOR_INSTRUCTION,
    output_key="user_needs",
    sub_agents=[sequential_agent_loop1, sequential_agent_loop2],
    generate_content_config=types.GenerateContentConfig(temperature=0.5),
)

root_agent = orchestrator_agent


# --- Sub Agent 6: Refactoring agent used in loop 2 of requirements engineering ---

