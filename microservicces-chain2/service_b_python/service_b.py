from __future__ import annotations
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import httpx
import uvicorn

app = FastAPI(title="Service B (Python)", version="1.0")


class TraceItem(BaseModel):
    service: str
    language: str
    info: Dict[str, Any] = {}
    

class Payload(BaseModel):
    message: str
    trace: List[TraceItem] = Field(default_factory=list)


@app.get("/ping")
def ping():
    return {"status": "ok", "service": "service-b", "message": "pong"}




@app.post("/stepB")
async def step_b(payload: Payload):
    
    reversed_msg = payload.message[::-1]

    
    payload.trace.append(TraceItem(
        service="service-b",
        language="Python (FastAPI)",
        info={"reversed": True},
       
    ))
    payload.message = reversed_msg

   
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(5.0, connect=2.0)) as client:
            rep = await client.post("http://127.0.0.1:9003/stepC", json=payload.model_dump())
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Service C introuvable: {e}")

    if rep.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Erreur Service C: {rep.text}")

    return rep.json()

if __name__ == "__main__":
    uvicorn.run("service_b:app", host="127.0.0.1", port=9002, reload=True)
