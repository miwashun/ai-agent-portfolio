from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from app.ai_client import generate_chat_reply

app = FastAPI()


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def index():
    return FileResponse("app/static/index.html")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    messages = [message.dict() for message in request.messages]
    reply = generate_chat_reply(messages)
    return ChatResponse(reply=reply)
