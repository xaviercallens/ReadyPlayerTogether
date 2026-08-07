# FastAPI wrapper for the Gemini 3.1 Pro QA Agent
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Server_AI.gemini_qa_agent import QAskillsWorker

worker = QAskillsWorker()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(worker.start())
    yield
    await worker.stop()
    task.cancel()

app = FastAPI(title="Gemini QA & Architecture Service", lifespan=lifespan)

class ReviewRequest(BaseModel):
    file_path: str

class ReviewResponse(BaseModel):
    result: str

async def _enqueue_and_wait(task_type: str, file_path: str) -> str:
    fut = asyncio.get_event_loop().create_future()
    def cb(res: str):
        if not fut.done():
            fut.set_result(res)
    await worker.queue.put({"type": task_type, "file": file_path, "callback": cb})
    return await fut

@app.post("/api/qa/review", response_model=ReviewResponse)
async def review_endpoint(req: ReviewRequest):
    res = await _enqueue_and_wait("review", req.file_path)
    return ReviewResponse(result=res)

@app.post("/api/qa/unittest", response_model=ReviewResponse)
async def unittest_endpoint(req: ReviewRequest):
    res = await _enqueue_and_wait("unittest", req.file_path)
    return ReviewResponse(result=res)

@app.post("/api/qa/improve", response_model=ReviewResponse)
async def improve_endpoint(req: ReviewRequest):
    res = await _enqueue_and_wait("improve", req.file_path)
    return ReviewResponse(result=res)
