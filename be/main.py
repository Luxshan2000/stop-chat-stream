import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from be.configs.database import Base, engine, get_db
from be.db.abort_signal_crud import delete_by_id, get_by_id, insert, update_flag_by_id
from be.models.chat import AbortRequest, ChatRequest
from be.services.memory_service import clients, remove_client, set_flag, store_client
from be.utils.logging import get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.delete_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # end cleanup code can go here


app = FastAPI(lifespan=lifespan)

logger = get_logger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat/")
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    model = request.model
    messages = request.messages
    stream = request.stream
    request_id = request.request_id

    client = AsyncOpenAI()

    # In Memory Approach: Start
    # store_client(request_id=request_id)
    # In Memory Approach: End

    # DB Approach with PSQL: Start
    await insert(session=db, id=request_id, flag=False)
    # DB Approach with PSQL: End

    res = await client.chat.completions.create(
        model=model, messages=messages, stream=stream
    )

    async def generate_response():
        async for chunk in res:
            content = chunk.choices[0].delta.content

            # In Memory Approach: Start
            # if clients[request_id]:
            #     logger.info("here")
            #     await client.close()
            #     remove_client(request_id=request_id)
            #     return
            # In Memory Approach: End

            # DB Approach with PSQL: Start
            abort = await get_by_id(session=db, id=request_id)
            await db.refresh(abort)
            logger.info(f"{request_id} - {abort.flag}")
            if abort.flag:
                await client.close()
                await delete_by_id(session=db, id=request_id)
                return
            # DB Approach with PSQL: End

            if content:
                yield content

        await client.close()

        # In Memory Approach: Start
        # remove_client(request_id=request_id)
        # In Memory Approach: End

        # DB Approach with PSQL: Start
        await delete_by_id(session=db, id=request_id)
        # DB Approach with PSQL: End

    return StreamingResponse(generate_response(), media_type="text/plain")


@app.post("/abort/")
async def abort_stream(request: AbortRequest, db: AsyncSession = Depends(get_db)):
    request_id = request.request_id
    logger.info(f"update: {request_id}")

    # In Memory Approach: Start
    # if request_id in clients:
    #     set_flag(request_id=request_id)
    #     return {"message": f"Streaming for request {request_id} will be aborted."}
    # In Memory Approach: End

    # DB Approach with PSQL: Start
    if await update_flag_by_id(session=db, id=request_id, new_flag=True):
        return {"message": f"Streaming for request {request_id} will be aborted."}
    # DB Approach with PSQL: End

    else:
        raise HTTPException(status_code=404, detail="Request ID not found")


@app.get("/")
async def root():
    return {"message": "Chat API is running"}
