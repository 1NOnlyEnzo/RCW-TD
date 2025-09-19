from __future__ import annotations
from fastapi import FastAPI, Query
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from datetime import datetime

app = FastAPI(title="Gateway", version="1.0")

class Inbound(BaseModel):   
    message: str

class Payload(BaseModel):   
    message: str
    trace: list


@app.get("/ping")
def ping():
    return {"status": "ok", "service": "gateway"}

@app.post("/api/chain")
async def chain(body: Inbound):
    
    payload = {"message": body.message, "trace": []}

    
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post("http://127.0.0.1:9001/stepA", json=payload)
    except Exception:
        raise HTTPException(status_code=502, detail="Service A introuvable")

    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Erreur de Service A")

    data = r.json()

    
    data["trace"].append({
        "service": "gateway",
        "info": "dernier passage",
        
    })

    
    return data
