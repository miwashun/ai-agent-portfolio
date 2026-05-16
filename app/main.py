from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse

from app import models
from app.ai_client import generate_chat_reply
from app.crud import create_conversation, create_message
from app.database import Base, SessionLocal, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    conversation_id: int | None = None
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    reply: str
    conversation_id: int


@app.get("/")
def index():
    return FileResponse("app/static/index.html")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    db = SessionLocal()
    try:
        conversation_id = request.conversation_id
        if conversation_id is None:
            conversation = create_conversation(db)
            conversation_id = conversation.id

        latest_user_message = request.messages[-1]
        create_message(
            db,
            conversation_id=conversation_id,
            role=latest_user_message.role,
            content=latest_user_message.content,
        )

        messages = [message.dict() for message in request.messages]
        reply = generate_chat_reply(messages)

        create_message(
            db,
            conversation_id=conversation_id,
            role="assistant",
            content=reply,
        )

        return ChatResponse(reply=reply, conversation_id=conversation_id)
    finally:
        db.close()
