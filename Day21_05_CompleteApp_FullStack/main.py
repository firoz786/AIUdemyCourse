"""
Day 21.05 - Complete App (Full Stack).

This is the final FastAPI server for the complete full-stack application.
It serves the static frontend, exposes a simple one-shot `/chat` endpoint,
and exposes a `/research` endpoint that streams the agent's live progress
events (plan, step, tool, verification, completion) to the browser via
Server-Sent Events (SSE) while the background research task runs in a
separate thread.
"""

import asyncio
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from agent import research_agent, run_agent
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


# Create the SSE event stream used by the frontend's "research" view to
# show the agent's live progress as it works.
@app.get("/research")
async def research(topic: str):
    # Queue used to pass progress events from the background research
    # thread into the async generator that streams them to the client.
    queue = asyncio.Queue()

    def progress_callback(event):
        # Called from the background thread running research_agent; adds
        # the event onto the asyncio queue for event_stream() to pick up.
        queue.put_nowait(event)

    async def event_stream():
        # Run the blocking research_agent loop in a background thread (8
        # max steps for this streaming demo) so this async generator stays
        # free to keep yielding queued progress events.
        task = asyncio.create_task(
            asyncio.to_thread(
                research_agent,
                topic,
                8,
                progress_callback
            )
        )

        while True:
            # Stop once the background task has finished and every queued
            # event has been drained and sent to the client.
            if task.done() and queue.empty():
                break

            try:
                # Wait briefly for the next progress event; each event is
                # sent as one Server-Sent Events (SSE) "data:" frame, which
                # the browser's EventSource API receives incrementally.
                event = await asyncio.wait_for(
                    queue.get(),
                    timeout=0.5
                )

                yield (
                    "data: "
                    + json.dumps(event)
                    + "\n\n"
                )

            except asyncio.TimeoutError:
                # No event yet; loop back and check if the task finished.
                continue

        # Pipeline finished: send the final research report as one last
        # SSE event.
        result = await task

        yield (
            "data: "
            + json.dumps({
                "type": "complete",
                "report": result
            })
            + "\n\n"
        )

    # media_type="text/event-stream" tells the browser this is an SSE
    # stream, which FastAPI/Starlette keeps open and flushes incrementally.
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )
