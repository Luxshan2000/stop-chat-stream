import os
from openai import AsyncOpenAI
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from be.services.memory_service import clients, store_client, remove_client, set_flag
from be.utils.logging import get_logger
from be.models.chat import ChatRequest, AbortRequest

app = FastAPI()

logger = get_logger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code can go here
    yield
    # end cleanup code can go here


@app.post("/chat/")
async def chat(request: ChatRequest):
    model = request.model
    messages = request.messages
    stream = request.stream
    request_id = request.request_id

    logger.info(model)

    client = AsyncOpenAI()
    
    # Store client and abort flag in memory
    clients[request_id] = {"client": client, "abort_flag": False}
    store_client(request_id=request_id)
    
    res = await client.chat.completions.create(model=model, messages=messages, stream=stream)

    async def generate_response():
        async for chunk in res:
            content = chunk.choices[0].delta.content
            if clients[request_id]["abort_flag"]:
                await client.close()
                remove_client(request_id=request_id)
                return
            if content:
                yield content

        await client.close()
        remove_client(request_id=request_id)
    return StreamingResponse(generate_response(), media_type="text/plain")

@app.post("/abort/")
async def abort_stream(request: AbortRequest):
    request_id=request.request_id
    if request.request_id in clients:
        set_flag(request_id=request_id)
        return {"message": f"Streaming for request {request_id} will be aborted."}
    else:
        raise HTTPException(status_code=404, detail="Request ID not found")

@app.get("/")
async def root():
    return {"message": "Chat API is running"}
