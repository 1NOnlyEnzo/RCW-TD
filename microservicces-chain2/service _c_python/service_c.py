from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uvicorn

app = FastAPI(title="Service C")


class Payload(BaseModel):
    message: str
    trace: list = Field(default_factory=list)  

@app.get("/ping")
def ping():
    return {"status": "ok", "service": "service-c"}

@app.post("/stepC")
def step_c(payload: Payload):
   
    length = len(payload.message)

    
    payload.trace.append({
        "service": "service-c",
        "language": "Python",
        "info": {"appended_len": length},
        
    })

    
    return payload

if __name__ == "__main__":
    uvicorn.run("service_c:app", host="127.0.0.1", port=9003, reload=True)
