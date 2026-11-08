"""
Day 20.04 - Deployment-ready FastAPI app (health/readiness, requirements).

This script is nearly identical to Day20_03's main.py, but belongs to the
"deployment" lesson: paired with requirements.txt, it shows a FastAPI
service ready to be deployed, with a startup/shutdown lifespan hook plus
"/health" (liveness) and "/ready" (readiness - checks Ollama is reachable)
endpoints that a deployment platform (e.g. Docker/Kubernetes) can probe.
Run with `uvicorn main:app --reload`.
"""

from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException

from agent import agent
from schemas import ChatRequest, ChatResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code before `yield` runs once at startup; code after `yield` runs
    # once at shutdown. This replaces the older @app.on_event("startup")
    # / @app.on_event("shutdown") decorators (deprecated in FastAPI).
    print("Application starting...")

    yield

    print("Application shutting down...")


# Create the FastAPI application object; this is what uvicorn runs.
app = FastAPI(
    title="AI Agent API",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health():
    # Simple liveness check: if this endpoint responds at all, the
    # process is up (does not check downstream dependencies like Ollama).
    return {
        "status": "ok"
    }


@app.get("/ready")
async def ready():
    # Readiness check: confirm the Ollama server is actually reachable
    # before telling callers/orchestrators that we can serve traffic.
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:11434/api/tags",
                timeout=2.0
            )

        if response.status_code == 200:
            return {
                "status": "ready"
            }

        return {
            "status": "not_ready"
        }

    except Exception:
        # Ollama unreachable/timed out - report "not_ready" instead of
        # letting the exception bubble up as a 500 error.
        return {
            "status": "not_ready"
        }


@app.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):
    # Request flow: FastAPI validates the incoming JSON into ChatRequest,
    # we forward the message to the agent, and return a validated
    # ChatResponse - or a clean HTTP error if anything goes wrong.
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

        return ChatResponse(
            answer=answer
        )

    except Exception as exc:
        # Log the full error for developers/ops, but hide the details
        # from the API caller behind a generic, user-facing message.
        print(f"Agent execution failed: {exc}")

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed"
        )