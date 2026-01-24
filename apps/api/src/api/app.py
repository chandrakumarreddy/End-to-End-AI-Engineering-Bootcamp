"""API server"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

from api.core.config import config
from api.routes.endpoints import api_router
from api.routes.middleware import RequestIDMiddleware


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

# add middleware

app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/chat')
def chat(request: Request, payload: ChatRequest) -> ChatResponse:
    """Chat endpoint."""
    try:
        result = run_llm(payload.provider, payload.model, payload.messages)
        return ChatResponse(message=result)
    except Exception as e:
        logger.error(e)
        return ChatResponse(message=str(e))


app.include_router(api_router, prefix='/rag', tags=['rag'])
