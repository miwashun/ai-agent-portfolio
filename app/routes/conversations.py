from typing import cast

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import get_conversation, get_conversation_messages
from app.dependencies import get_db
from app.schemas import ConversationMessageResponse, ConversationResponse

router = APIRouter()


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
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
