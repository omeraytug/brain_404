from dotenv import load_dotenv
from pydantic_ai import Agent

from backend.agent.prompts import SYSTEM_PROMPT
from backend.constants import MODEL_MEDIUM
from backend.schemas import ChatResponse

load_dotenv()

wired_al_agent = Agent(
    model=MODEL_MEDIUM, system_prompt=SYSTEM_PROMPT, output_type=ChatResponse
)


async def chat(question: str) -> ChatResponse:
    result = await wired_al_agent.run(question)
    return result.output
