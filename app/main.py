from typing import cast

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import models  # noqa: F401
from app.crud import get_conversation, get_conversation_messages
from app.database import Base, engine
from app.dependencies import get_db
from app.routes.chat import router as chat_router
from app.schemas import ConversationMessageResponse, ConversationResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(chat_router)


@app.get("/")
def index():
    return FileResponse("app/static/index.html")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def read_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = get_conversation(db, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = get_conversation_messages(db, conversation_id)
    return ConversationResponse(
        conversation_id=conversation_id,
        messages=[
            ConversationMessageResponse(
                role=cast(str, message.role),
                content=cast(str, message.content),
            )
            for message in messages
        ],
    )
