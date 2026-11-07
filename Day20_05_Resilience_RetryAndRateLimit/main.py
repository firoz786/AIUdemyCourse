import asyncio
import logging
import time
import uuid
from collections import defaultdict, deque
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request
from tenacity import retry, stop_after_attempt, wait_exponential

from agent import agent
from schemas import ChatRequest, ChatResponse
import os

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("ai_agent")


REQUEST_LIMIT = 10
WINDOW_SECONDS = 60

request_times = defaultdict(deque)


def check_rate_limit(client_id: str) -> bool:
    now = time.time()

    times = request_times[client_id]

    while times and now - times[0] > WINDOW_SECONDS:
        times.popleft()

    if len(times) >= REQUEST_LIMIT:
        return False

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
    return {
        "status": "ok"
    }


@app.get("/ready")
async def ready():

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

    request_id = str(uuid.uuid4())

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

        logger.error(
            "request_timeout request_id=%s",
            request_id
        )

        raise HTTPException(
            status_code=504,
            detail="Agent request timed out"
        )

    except Exception:

        logger.exception(
            "agent_failed request_id=%s",
            request_id
        )

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed"
        )

