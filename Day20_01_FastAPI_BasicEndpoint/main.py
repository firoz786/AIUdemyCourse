from fastapi import FastAPI
from pydantic import BaseModel

from agent import agent


app = FastAPI(
    title="AI Agent API",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
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

    return {
        "answer": result["messages"][-1].content
    }
