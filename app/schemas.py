from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    conversation_id: int | None = None
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    reply: str
    conversation_id: int


class ConversationMessageResponse(BaseModel):
    role: str
    content: str


class ConversationResponse(BaseModel):
    conversation_id: int
    messages: list[ConversationMessageResponse]
