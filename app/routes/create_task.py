from fastapi import APIRouter, Body, Query, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os

from app.worker import create_task

router = APIRouter()

@router.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})