from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from httpx import AsyncClient
from dotenv import load_dotenv
import os

load_dotenv()
base_url = os.getenv("BASE_URL")
token = os.getenv("TOKEN")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.post("/api/chat")
async def chat(request: Request):
    req = await request.json()
    user = req.get("user")
    query = req.get("query")

    url = f"{base_url}/v1/chat-messages"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "user": user,
        "response_mode": "streaming",  # 1. 关键改动
        "inputs": {},
        "query": query,
    }

    async def event_stream():
        async with AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=data, headers=headers) as r:
                async for chunk in r.aiter_bytes():
                    yield chunk

    return StreamingResponse(event_stream(), media_type="text/event-stream")


app.mount("/", StaticFiles(directory="public", html=True))


if __name__ == "__main__":
    import multiprocessing
    import uvicorn

    multiprocessing.freeze_support()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4)
