from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime, timezone
from ..database.database import get_db, Conversation
from sqlalchemy.orm import Session

from app.llm.llm_setup import llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.chatbot.chatbot import process_user_input

router = APIRouter()

chat_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

class ChatRequest(BaseModel):
    question: str
    docs: List[str] = []
    chat_history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    response: str

class ConversationResponse(BaseModel):
    id: int
    user_input: str
    bot_response: str
    timestamp: datetime

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(data: ChatRequest, db: Session = Depends(get_db)):
    try:
        response = process_user_input(data.question, data.chat_history)
        
        conversation = Conversation(
            user_input=data.question,
            bot_response=response,
            timestamp=datetime.now(timezone.utc)        )
        db.add(conversation) #prepara mas n coloca no db
        db.commit() #confima a transacao
        db.refresh(conversation) #att os valores (id por ex)

        return ChatResponse(response=response)
    
    except Exception as e:
        db.rollback()
        return ChatResponse(response=f"Erro ao processar: {str(e)}")
    
@router.get("/info", response_model=ChatResponse)
def info_endpoint():
    try:
        welcome_message = """
👋 Olá! Sou especialista em MARKETING DIGITAL.
Posso ajudar com:
- Vendas online
- Redes sociais
- Publicidade
- SEO
Qualquer dúvida relacionada a esses tópicos, estarei à disposição para ajudar!
        """
        return ChatResponse(response=welcome_message.strip())
    
    except Exception as e:
        return ChatResponse(response=f"Erro ao processar a solicitação: {str(e)}")

@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(db: Session = Depends(get_db)):
    conversations = db.query(Conversation).order_by(Conversation.timestamp.desc()).all()
    return conversations