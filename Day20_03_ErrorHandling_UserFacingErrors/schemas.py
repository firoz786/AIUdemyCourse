"""
Day 20.03 - Pydantic schemas for request/response validation.

Same role as Day20_02's schemas.py: defines the JSON shapes for the
`/chat` endpoint's request and response bodies.
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    # The user's chat message; FastAPI rejects requests missing this field.
    message: str


class ChatResponse(BaseModel):
    # The agent's final text answer, returned to the caller as JSON.
    answer: str
