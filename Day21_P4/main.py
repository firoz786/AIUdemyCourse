from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from agent import run_agent
from schemas import ChatRequest, ChatResponse

import asyncio
import json

from fastapi.responses import StreamingResponse

from agent import research_agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Research AI application")
    yield
    print("Shutting down Research AI application")


app = FastAPI(
    title="Research AI Agent",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static",
)


@app.get("/")
async def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        result = await run_in_threadpool(run_agent, request.message)

        return ChatResponse(
            response=result
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


#Create the event stream
@app.get("/research")
async def research(topic: str):

    queue = asyncio.Queue()

    def progress_callback(event):

        queue.put_nowait(event)


    async def event_stream():

        task = asyncio.create_task(
            asyncio.to_thread(
                research_agent,
                topic,
                8,
                progress_callback
            )
        )


        while True:

            if task.done() and queue.empty():
                break


            try:

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

                continue


        result = await task

        yield (
            "data: "
            + json.dumps({
                "type": "complete",
                "report": result
            })
            + "\n\n"
        )


    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )
