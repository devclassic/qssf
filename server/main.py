from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.post("/chat")
async def chat(request: Request):
    req = await request.json()
    user = req.get("user")
    query = req.get("query")
    url = "http://ai.btqssf.cn/v1/chat-messages"
    headers = {"Authorization": "Bearer app-aPYc1Mrmv4UrmFY28qVHODbO"}
    data = {
        "user": user,
        "response_mode": "blocking",
        "inputs": {},
        "query": query,
    }
    async with AsyncClient(timeout=None) as client:
        res = await client.post(url, json=data, headers=headers)
        result = res.json()
    return {
        "success": True,
        "message": "聊天成功",
        "data": result.get("answer", ""),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=8)
