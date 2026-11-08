"""
Day 21.04 - Tools and Schema with UI.

FastAPI server that connects the static web frontend to the research
agent, whose tools now expose richer schemas (docstrings/typed arguments)
for the model to use. Serves the frontend's HTML/CSS/JS and exposes a
`/chat` endpoint that runs the (blocking) research agent in a thread pool
and returns its final report as a plain JSON response.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from agent import run_agent
from schemas import ChatRequest, ChatResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once at startup and once at shutdown; used here just for
    # console logging of the app lifecycle.
    print("Starting Research AI application")
    yield
    print("Shutting down Research AI application")


app = FastAPI(
    title="Research AI Agent",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the browser frontend to call this API without CORS errors during
# local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend's static assets (CSS/JS) under /static.
app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static",
)


@app.get("/")
async def home():
    # Serve the frontend's main HTML page when the browser visits "/".
    return FileResponse("frontend/index.html")


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Reject empty/whitespace-only messages before doing any real work.
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        # run_agent is a blocking/synchronous function, so it's offloaded
        # to a thread pool to avoid blocking FastAPI's async event loop.
        result = await run_in_threadpool(run_agent, request.message)

        return ChatResponse(
            response=result
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )