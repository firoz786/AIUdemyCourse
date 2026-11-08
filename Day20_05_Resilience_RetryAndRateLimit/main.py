"""
Day 20.05 - Resilience: retries, timeouts, and rate limiting.

This is the most advanced FastAPI example in Day 20. On top of the
earlier health/readiness endpoints and error handling, it adds:
retrying a failed agent call once with exponential backoff (tenacity),
giving up on an agent call that takes too long (asyncio.wait_for), a
simple in-memory per-client rate limiter (sliding time window), and
structured logging with a unique request_id for every call, so the
"/chat" endpoint degrades gracefully under load or transient failures.
Run with `uvicorn main:app --reload`.
"""

import asyncio
import logging
import os
import time
import uuid
from collections import defaultdict, deque
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request
from tenacity import retry, stop_after_attempt, wait_exponential

from agent import agent
from schemas import ChatRequest, ChatResponse

# Where the Ollama server lives, used by the /ready endpoint below.
OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

# Configure structured logging so every log line has a timestamp/level,
# which makes it much easier to correlate requests in production.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("ai_agent")

# Simple sliding-window rate limit settings: at most REQUEST_LIMIT
# requests per client within any WINDOW_SECONDS window.
REQUEST_LIMIT = 10
WINDOW_SECONDS = 60

# Tracks recent request timestamps per client IP (in-memory only - resets
# if the process restarts, and isn't shared across multiple workers).
request_times = defaultdict(deque)


def check_rate_limit(client_id: str) -> bool:
    # Returns True if this client is still within its request budget,
    # False if they must be rejected (HTTP 429).
    now = time.time()

    times = request_times[client_id]

    # Drop timestamps that have fallen outside the sliding window.
    while times and now - times[0] > WINDOW_SECONDS:
        times.popleft()

    if len(times) >= REQUEST_LIMIT:
        return False

    # Record this request and allow it through.
    times.append(now)

    return True


@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=4
    )
)
async def run_agent(message: str):
    # Wrapper around the agent call so `tenacity` can automatically retry
    # it (up to 2 attempts total, waiting longer between each retry) if
    # it raises an exception - e.g. a transient network/model hiccup.
    return await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code before `yield` runs once at startup; code after `yield` runs
    # once at shutdown. This replaces the older @app.on_event("startup")
    # / @app.on_event("shutdown") decorators (deprecated in FastAPI).
    logger.info("application_starting")

    yield

    logger.info("application_shutting_down")


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
                f"{OLLAMA_BASE_URL}/api/tags",
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
async def chat(
    request: Request,
    body: ChatRequest
):
    # Request flow: FastAPI validates `body` against ChatRequest; we also
    # take the raw `Request` object so we can read the caller's IP for
    # rate limiting. A unique request_id ties all log lines for this
    # call together, which is invaluable when debugging in production.
    request_id = str(uuid.uuid4())

    client_id = request.client.host

    # Reject the request early (before calling the agent) if this client
    # has made too many requests recently.
    if not check_rate_limit(client_id):
        logger.warning(
            "rate_limit_exceeded request_id=%s client=%s",
            request_id,
            client_id
        )

        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )

    start_time = time.perf_counter()

    logger.info(
        "request_started request_id=%s",
        request_id
    )

    try:
        # Run the (auto-retrying) agent call, but give up entirely if it
        # takes longer than 30 seconds so one slow request can't hang the
        # whole endpoint.
        result = await asyncio.wait_for(
            run_agent(body.message),
            timeout=30
        )

        answer = result["messages"][-1].content

        duration = time.perf_counter() - start_time

        logger.info(
            "request_completed request_id=%s duration=%.2fs",
            request_id,
            duration
        )

        return ChatResponse(
            answer=answer
        )

    except asyncio.TimeoutError:
        # The agent call (including its retries) took too long overall.
        logger.error(
            "request_timeout request_id=%s",
            request_id
        )

        raise HTTPException(
            status_code=504,
            detail="Agent request timed out"
        )

    except Exception:
        # Any other failure (even after retries) - log full details
        # server-side, but return a clean, user-facing error message.
        logger.exception(
            "agent_failed request_id=%s",
            request_id
        )

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed"
        )

