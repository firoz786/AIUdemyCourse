"""
Day 20.02 - Pydantic schemas for request/response validation.

This module defines the JSON shapes used by the FastAPI "/chat" endpoint:
ChatRequest for the incoming body and ChatResponse for the outgoing
body. FastAPI uses these (Pydantic v2) models to validate input, document
the API (OpenAPI/Swagger), and serialize output automatically.
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    # The user's chat message; FastAPI rejects requests missing this field.
    message: str


class ChatResponse(BaseModel):
    # The agent's final text answer, returned to the caller as JSON.
    answer: str
