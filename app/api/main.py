from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Chatbot de Marketing Digital")

app.include_router(router)
