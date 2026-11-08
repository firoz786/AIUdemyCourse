"""
Day 21.03 - Frontend Agent Integration.

Pydantic request/response models used by the `/chat` endpoint that wires
the frontend (served as static files) directly to the research agent
defined in agent.py.
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    # The user's chat message sent from the frontend.
    message: str


class ChatResponse(BaseModel):
    # The agent's final text/report returned to the frontend.
    response: str

