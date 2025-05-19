import uvicorn
from fastapi import FastAPI
from app.api.api import router

app = FastAPI(title="Authentication Service")

# Include API router. 
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)