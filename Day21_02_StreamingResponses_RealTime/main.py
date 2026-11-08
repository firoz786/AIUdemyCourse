"""
Day 21.02 - Streaming Responses (Real Time).

This lesson's main.py is a deliberately minimal FastAPI app: it just serves
the static frontend and a health check. The actual streaming (Server-Sent
Events) research endpoint is introduced in later lessons/files — this file
focuses on the basic app skeleton (lifespan, static file serving) the
streaming feature will be layered onto.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once at startup and once at shutdown, used here just to log the
    # app's lifecycle to the console.
    print("Starting Research AI application")

    yield

    print("Shutting down Research AI application")


app = FastAPI(
    title="Research AI Agent",
    version="1.0.0",
    lifespan=lifespan,
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
    return FileResponse(
        "frontend/index.html"
    )


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }

