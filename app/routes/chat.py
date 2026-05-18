from typing import cast

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai_client import generate_chat_reply
from app.crud import create_conversation, create_message
from app.dependencies import get_db
from app.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    conversation_id = request.conversation_id
    if conversation_id is None:
        conversation = create_conversation(db)
        conversation_id = cast(int, conversation.id)

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
