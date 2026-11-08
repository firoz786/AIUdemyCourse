"""
Day 21.05 - Complete App (Full Stack).

Pydantic request/response models used by the `/chat` endpoint of the
final, complete full-stack application (frontend + agent + tools +
streaming `/research` endpoint).
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    # The user's chat message sent from the frontend.
    message: str


class ChatResponse(BaseModel):
    # The agent's final text/report returned to the frontend.
    response: str

