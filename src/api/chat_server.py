from fastapi import FastAPI, HTTPException
from src.services.chat_service import ChatService
from src.components.vectorstore import VectorStore
from src.config.configuration import ConfigurationManager
from src.utils.blob_sync import download_vectorstore
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Lucid Chat")

# Shared, app-wide state — built once, reused across every request
state = {}


class ChatRequest(BaseModel):
    user_message: str
    anchor_paper_id: Optional[str] = None


def build_chat_service() -> ChatService:
    download_vectorstore()
    config_manager = ConfigurationManager()
    vectorstore_config = config_manager.get_vectorstore_config()
    vectorstore = VectorStore(vectorstore_config)
    return ChatService(vectorstore)


@app.on_event("startup")
def startup_event():
    state["chat_service"] = build_chat_service()


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        reply = state["chat_service"].chat(request.user_message, request.anchor_paper_id)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/internal/reload-vectorstore")
def reload_vectorstore():
    try:
        state["chat_service"] = build_chat_service()
        return {"message": "Vectorstore reloaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))