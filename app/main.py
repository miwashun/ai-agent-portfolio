from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401
from app.database import Base, engine
from app.routes.chat import router as chat_router
from app.routes.conversations import router as conversations_router
from app.routes.health import router as health_router
from app.routes.pages import router as pages_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(chat_router)
app.include_router(conversations_router)
app.include_router(health_router)
app.include_router(pages_router)
