from pydantic import BaseModel

class ChatInput(BaseModel):
  question: str
  chat_history: list[dict] = []

class ChatOutput(BaseModel):
  response: str
  chat_history: list[dict]