from fastapi import FastAPI, HTTPException

from agent import agent
from schemas import ChatRequest, ChatResponse


app = FastAPI(
    title="AI Agent API",
    version="1.0.0"
)


@app.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(request: ChatRequest):

    try:
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

        answer = result["messages"][-1].content

        return ChatResponse(
            answer=answer
        )

    except Exception as exc:
        print(f"Agent execution failed: {exc}")

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed"
        )
