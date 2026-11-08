"""
Day 21.01 - Frontend Web UI.

Pydantic models describing the JSON shapes used by the FastAPI endpoints:
the one-shot chat request/response, and the individual event objects sent
over the `/research` Server-Sent Events (SSE) stream.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    # Incoming request body for the one-shot /chat endpoint.
    message: str = Field(
        ...,
        min_length=1,
        description="User research topic or prompt."
    )


class ChatResponse(BaseModel):
    # Response body returned by the /chat endpoint.
    response: str = Field(
        ...,
        description="Final markdown research report."
    )


class StreamEvent(BaseModel):
    # Shape of each JSON object sent as an SSE "data:" frame while the
    # agent is researching (plan/step/tool/verification/complete/error).
    type: str = Field(..., description="Type of event emitted during execution.")
    message: Optional[str] = Field(None, description="Human readable event message.")
    tool: Optional[str] = Field(None, description="Executed tool identifier.")
    step: Optional[int] = Field(None, description="Current agent iteration step.")
    plan: Optional[str] = Field(None, description="Full strategic research plan.")
    report: Optional[str] = Field(None, description="Generated final markdown report.")
    details: Optional[Dict[str, Any]] = Field(None, description="Execution metadata.")