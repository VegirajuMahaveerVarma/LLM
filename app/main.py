from fastapi import FastAPI
from app.config import settings
from app.models import ChatRequest, ChatResponse
from app.services.orchestrator import respond

app = FastAPI(title=settings.app_name, version=settings.version)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name, "version": settings.version}

@app.post("/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return respond(request)
