"""Models for the Rag endpoint."""
from pydantic import BaseModel, Field


class RagRequest(BaseModel):
    """Request model for the Rag endpoint."""
    query: str = Field(..., description="Query to be sent to the LLM")


class RagResponse(BaseModel):
    """Response model for the Rag endpoint."""
    request_id: str = Field(..., description="Request ID")
    answer: str = Field(..., description="Answer to the query")
