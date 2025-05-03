from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from app.llm.llm_setup import llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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
        context = "\n".join(data.docs)
        messages = chat_prompt.format_messages(
            chat_history=data.chat_history,
            question=f"{data.question}\n\n[Contexto de apoio]:\n{context}"
        )

        response = llm.invoke(messages)
        return ChatResponse(response=response.content)
    except Exception as e:
        return ChatResponse(response=f"Erro ao processar: {str(e)}")
