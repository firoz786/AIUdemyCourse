"""
Day 20.02 - Input validation with Pydantic schemas.

This script builds on Day20_01 by moving the request/response shapes into
a separate schemas.py module (ChatRequest / ChatResponse), using
`response_model` so FastAPI validates and documents the outgoing JSON
too, and adding basic error handling: if the agent raises an exception,
the endpoint returns a clean HTTP 500 with a user-facing message instead
of leaking a stack trace. Run with `uvicorn main:app --reload`.
"""

from fastapi import FastAPI, HTTPException

from agent import agent
from schemas import ChatRequest, ChatResponse


# Create the FastAPI application object; this is what uvicorn runs.
app = FastAPI(
    title="AI Agent API",
    version="1.0.0"
)


@app.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):
    # Request flow: FastAPI validates the incoming JSON against
    # ChatRequest (rejecting malformed bodies automatically), then we
    # forward the validated message to the agent and await its reply.
    try:
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.message
                    }
                ]
            }
        )

        answer = result["messages"][-1].content

        # Wrap the answer in ChatResponse so FastAPI validates/serializes
        # the outgoing JSON the same way it validated the incoming body.
        return ChatResponse(
            answer=answer
        )

    except Exception as exc:
        # Log the real error for developers, but don't expose internal
        # details to the API caller - return a safe, generic message.
        print(f"Agent execution failed: {exc}")

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed"
        )
