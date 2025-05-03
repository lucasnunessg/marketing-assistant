from fastapi import FastAPI
from app.api.endpoints import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Chatbot de Marketing Digital")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
