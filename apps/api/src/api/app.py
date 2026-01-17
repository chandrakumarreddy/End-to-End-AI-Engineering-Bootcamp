"""API server"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from pydantic import BaseModel

from api.core.config import config
from openai import OpenAI


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_llm(provider, model, messages):
    """Return LLM model based on provider and model"""
    print(messages)
    if provider and model:
        client = OpenAI(api_key=config.OPENAI_API_KEY,
                        base_url="https://openrouter.ai/api/v1",)
        model = 'nvidia/nemotron-3-nano-30b-a3b:free'
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            extra_body={"reasoning": {"enabled": False}}
        )
        return response.choices[0].message.content or ""
    else:
        return "Provider not supported"


class ChatRequest(BaseModel):
    """Chat model."""
    provider: str
    model: str
    messages: list[dict]


class ChatResponse(BaseModel):
    """Chat response."""
    message: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage lifespan events."""
    logger.info("Starting FastAPI application")
    yield
    logger.info("Shutting down FastAPI application")


app = FastAPI(title="Simple API", version="0.1.0", lifespan=lifespan)


@app.post('/chat')
def chat(request: Request, payload: ChatRequest) -> ChatResponse:
    """Chat endpoint."""
    try:
        result = run_llm(payload.provider, payload.model, payload.messages)
        return ChatResponse(message=result)
    except Exception as e:
        logger.error(e)
        return ChatResponse(message=str(e))
