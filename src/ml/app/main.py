from fastapi import FastAPI
from routes.chat import router as chat_router

app = FastAPI()
app.include_router(chat_router, prefix="/api")
