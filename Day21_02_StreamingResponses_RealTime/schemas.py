"""
Day 21.02 - Streaming Responses (Real Time).

Pydantic models for the research request/response payloads used once the
streaming `/research` endpoint is added on top of this lesson's app
skeleton.
"""

from pydantic import BaseModel


class ResearchRequest(BaseModel):
    # The topic the user wants the agent to research.
    topic: str


class ResearchResponse(BaseModel):
    # The final generated Markdown report.
    report: str

