from langchain_ollama import ChatOllama
from prompt.prompt import marketing_prompt

llm = ChatOllama(
    model="gemma:2b",
    temperature=0.2,  
    num_ctx=1024,
    num_thread=4
)

def ask_llm(question: str, docs: list[str]) -> str:
  context= "\n".join(docs)
  prompt = marketing_prompt.format(question=question, context=context)


  try:
    response = llm.invoke(prompt)
    return response.content
  except Exception as e:
    print(f"Erro completo: {str(e)}")
    return f"Erro ao processar: {str(e)}"