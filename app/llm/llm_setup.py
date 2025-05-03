from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="gemma:2b",
    temperature=0.2,  
    num_ctx=1024,
    num_thread=4
)