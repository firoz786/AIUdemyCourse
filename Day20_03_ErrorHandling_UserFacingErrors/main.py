from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException

from agent import agent
from schemas import ChatRequest, ChatResponse


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Application starting...")

    yield

    print("Application shutting down...")


app = FastAPI(
    title="AI Agent API",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


@app.get("/ready")
async def ready():

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
        return {
            "status": "not_ready"
        }


@app.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

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
        print(f"Agent execution failed: {exc}")

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed"


        )