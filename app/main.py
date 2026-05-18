from fastapi import FastAPI
from fastapi.responses import FileResponse

from app import models  # noqa: F401
from app.database import Base, engine
from app.routes.chat import router as chat_router
from app.routes.conversations import router as conversations_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(chat_router)
app.include_router(conversations_router)


@app.get("/")
def index():
    return FileResponse("app/static/index.html")


@app.get("/health")
def health_check():
    return {"status": "ok"}
