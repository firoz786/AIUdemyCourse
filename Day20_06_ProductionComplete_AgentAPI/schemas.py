"""
Day 20.06 - Production Complete Agent API.

Defines the Pydantic request/response models used by the FastAPI `/chat`
endpoint. FastAPI uses these to validate incoming JSON, generate API docs,
and serialize the outgoing response.
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    # The user's chat message sent in the request body.
    message: str


class ChatResponse(BaseModel):
    # The agent's final text answer returned to the caller.
    answer: str
