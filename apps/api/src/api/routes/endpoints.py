"""
Endpoints for the API.
"""

from fastapi import APIRouter, Request
from api.routes.models import RagRequest, RagResponse
from api.agents.retrieval_generation import rag_pipeline

api_router = APIRouter()


@api_router.post("/", response_model=RagResponse)
async def rag_endpoint(request: Request, payload: RagRequest):
    """Endpoint for the Rag endpoint."""
    answer_message = rag_pipeline(payload.query)

    return RagResponse(answer=answer_message or '', request_id=request.state.request_id)
