"""
Day 21.01 - Frontend Web UI.

This is the FastAPI server that puts a basic web frontend in front of the
research agent. It serves the static HTML/JS/CSS frontend, exposes a
simple `/chat` request/response endpoint for one-shot answers, and exposes
a `/research` endpoint that streams live progress events to the browser
using Server-Sent Events (SSE) while the agent works through its steps.
"""

import asyncio
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from agent import generate_report, research_agent, run_agent
from schemas import ChatRequest, ChatResponse
from tools import get_verified_research_notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once at startup and once at shutdown; used here just for
    # simple console logging of the server lifecycle.
    print("Starting Research AI server")
    yield
    print("Shutting down Research AI server")


app = FastAPI(
    title="Research AI Agent",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the frontend (served from any origin during local development) to
# call this API from the browser without being blocked by CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend's CSS/JS assets under /static.
app.mount("/static", StaticFiles(directory="frontend"), name="static")


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
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        # `run_agent` is a blocking/synchronous function, so we run it in a
        # thread pool to avoid blocking FastAPI's async event loop while
        # the (potentially slow) research agent runs.
        result = await run_in_threadpool(run_agent, request.message)
        return ChatResponse(response=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/research")
async def research(topic: str):
    # Reject empty/whitespace-only topics before starting the pipeline.
    if not topic.strip():
        raise HTTPException(status_code=400, detail="Topic parameter is required.")

    # Queue used to pass progress events from the background research
    # thread into the async generator that streams them to the client.
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()

    def progress_callback(event):
        # Called from the worker thread; `call_soon_threadsafe` safely
        # schedules the put onto the asyncio event loop running in the
        # main thread.
        loop.call_soon_threadsafe(queue.put_nowait, event)

    def run_pipeline():
        # Runs the full research loop (blocking), emitting progress events
        # as it goes, then synthesizes and returns the final report.
        research_agent(user_request=topic, max_steps=15, progress_callback=progress_callback)
        notes = get_verified_research_notes()
        if not notes:
            raise ValueError("No verified findings collected during research.")

        progress_callback({"type": "step", "message": "Synthesizing final Markdown report..."})
        return generate_report(user_request=topic, verified_notes=notes)

    async def event_stream():
        # Run the blocking pipeline in a background thread so this async
        # generator stays free to keep yielding queued progress events.
        task = asyncio.create_task(asyncio.to_thread(run_pipeline))

        while True:
            # Stop once the background task has finished and every queued
            # event has been drained and sent to the client.
            if task.done() and queue.empty():
                break

            try:
                # Wait briefly for the next progress event; each event is
                # sent as one Server-Sent Events (SSE) "data:" frame, which
                # the browser's EventSource API receives incrementally.
                event = await asyncio.wait_for(queue.get(), timeout=0.5)
                yield f"data: {json.dumps(event)}\n\n"
            except asyncio.TimeoutError:
                # No event yet; loop back and check if the task finished.
                continue

        try:
            # Pipeline finished successfully: send the final report as one
            # last SSE event.
            report_content = await task
            yield f"data: {json.dumps({'type': 'complete', 'report': report_content})}\n\n"
        except Exception as err:
            # Pipeline raised an exception: surface it to the client as an
            # error event instead of crashing the stream.
            yield f"data: {json.dumps({'type': 'error', 'message': str(err)})}\n\n"

    # media_type="text/event-stream" tells the browser this is an SSE
    # stream, which FastAPI/Starlette keeps open and flushes incrementally.
    return StreamingResponse(event_stream(), media_type="text/event-stream")