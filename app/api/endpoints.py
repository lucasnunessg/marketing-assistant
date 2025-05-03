from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from app.llm.llm_setup import llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.chatbot.chatbot import process_user_input

router = APIRouter()

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um especialista em marketing digital. Responda sempre com foco em vendas, redes sociais, tráfego e SEO."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

class ChatRequest(BaseModel):
    question: str
    docs: List[str] = []
    chat_history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(data: ChatRequest):
    try:
        response = process_user_input(data.question, data.chat_history)
        return ChatResponse(response=response)
    
    except Exception as e:
        return ChatResponse(response=f"Erro ao processar: {str(e)}")
