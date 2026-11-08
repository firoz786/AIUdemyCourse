"""
Day 20.06 - Production Complete Agent API.

This is the main FastAPI application that exposes the LangChain agent as a
production-style HTTP service. It adds the kind of operational concerns a
real deployment needs on top of a bare agent: structured logging, health and
readiness probes, a simple in-memory per-client rate limiter, automatic
retries around the (sometimes flaky) local LLM call, and an overall request
timeout so the `/chat` endpoint never hangs forever.
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

# Base URL of the local Ollama server, used by the /ready health check to
# confirm the model backend is actually reachable.
OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

# Configure a simple timestamped logger so every request can be traced in
# the console output (request started/completed/failed, with durations).
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("ai_agent")


# Very small sliding-window rate limiter: each client is allowed at most
# REQUEST_LIMIT requests per WINDOW_SECONDS. This is in-memory only (resets
# on restart and isn't shared across multiple server instances) but is
# enough to demonstrate the concept for teaching purposes.
REQUEST_LIMIT = 10
WINDOW_SECONDS = 60

# Maps client_id -> deque of request timestamps (one deque per client).
request_times = defaultdict(deque)


def check_rate_limit(client_id: str) -> bool:
    """Return True if client_id may make another request right now."""

    now = time.time()

    times = request_times[client_id]

    # Drop timestamps that have aged out of the rolling window.
    while times and now - times[0] > WINDOW_SECONDS:
        times.popleft()

    # Client has already used up their quota for this window.
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
    """Invoke the LangChain agent, retrying once on transient failures."""

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
    # Runs once when the FastAPI app starts up, then again (after the
    # `yield`) when it shuts down — useful for startup/teardown logging.
    logger.info("application_starting")

    yield

    logger.info("application_shutting_down")


app = FastAPI(
    title="AI Agent API",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health():
    # Liveness probe: just confirms the process is up and responding.
    return {
        "status": "ok"
    }


@app.get("/ready")
async def ready():
    # Readiness probe: confirms the Ollama model backend is reachable
    # before telling orchestration tooling (e.g. Kubernetes) to send
    # real traffic to this instance.
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
        # Any network error, timeout, etc. means the backend isn't ready.
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
    # Unique ID for this request so every log line can be correlated back
    # to the same chat call, even under concurrent traffic.
    request_id = str(uuid.uuid4())

    # Rate limiting is keyed by the caller's IP address.
    client_id = request.client.host

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
        # Hard timeout: don't let a stuck model call hang the request
        # forever, regardless of the retry logic inside run_agent.
        result = await asyncio.wait_for(
            run_agent(body.message),
            timeout=30
        )

        # The agent returns a list of messages; the last one is the
        # final answer produced by the model.
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
        logger.error(
            "request_timeout request_id=%s",
            request_id
        )

        raise HTTPException(
            status_code=504,
            detail="Agent request timed out"
        )

    except Exception:
        # Catch-all so unexpected agent/tool errors become a clean 500
        # instead of leaking a stack trace to the client.
        logger.exception(
            "agent_failed request_id=%s",
            request_id
        )

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed"
        )

