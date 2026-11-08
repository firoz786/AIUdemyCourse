"""
Day 21.04 - Tools and Schema with UI.

Pydantic request/response models used by the `/chat` endpoint. This
lesson's focus is on the tool function signatures/docstrings (the
"schema" the model sees) in agent.py/tools.py, while these Pydantic models
remain the simple HTTP-facing schema for the frontend <-> API contract.
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    # The user's chat message sent from the frontend.
    message: str


class ChatResponse(BaseModel):
    # The agent's final text/report returned to the frontend.
    response: str

