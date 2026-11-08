"""
Day 20.01 - Exposing a LangChain agent through a basic FastAPI endpoint.

This is the first Day 20 script: it shows the minimal code needed to turn
an in-process LangChain agent into a web service. It defines one POST
endpoint, "/chat", that accepts a JSON body with a "message" field,
forwards that message to the agent, and returns the agent's final reply
as JSON. Run this with `uvicorn main:app --reload` to start the server.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from agent import agent


# Create the FastAPI application object; this is what uvicorn runs.
app = FastAPI(
    title="AI Agent API",
    version="1.0.0"
)


# Pydantic model describing the expected JSON body of a chat request.
# FastAPI uses this to validate incoming requests automatically.
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    # Request flow: FastAPI parses/validates the incoming JSON into a
    # ChatRequest, we pass `request.message` to the agent as the user's
    # chat message, await the agent's (async) response, then return the
    # final answer as a JSON response body.
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

    # The agent's reply is the last message in the conversation list.
    return {
        "answer": result["messages"][-1].content
    }
