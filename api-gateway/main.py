import uvicorn
from fastapi import FastAPI, Request, Response
import httpx
from app.routes import router
from app.config import settings

app = FastAPI(title="API Gateway")

# Include API router
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)