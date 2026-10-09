from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import agent


app = FastAPI(
    title="Vehicle Lead Agent"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def root():
    return {
        "message": "Vehicle Lead Agent is running"
    }


@app.post("/vehicle-leads/chat")
async def vehicle_lead_chat(request: ChatRequest):
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.message,
                }
            ]
        }
    )

    content = result["messages"][-1].content

    if isinstance(content, list):
        response_text = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )
    else:
        response_text = content

    return {
        "response": response_text
    }