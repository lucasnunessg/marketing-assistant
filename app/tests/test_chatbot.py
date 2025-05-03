from app.chatbot.chatbot import process_user_input

# Fake para o LLM
class FakeLLM:
    def invoke(self, messages):
        return type("Response", (), {"content": "Resposta fake do LLM"})()

# Fake para o retriever
def fake_retriever(question):
    return ["Fake contexto 1", "Fake contexto 2"]

# Teste de processamento de input marketing
def test_process_user_input_marketing():
    question = "Como criar uma campanha no Facebook Ads?"
    chat_history = []
    # Usando o fake do retriever e do LLM
    response = process_user_input(question, chat_history, llm_instance=FakeLLM(), retriever=fake_retriever)
    assert isinstance(response, str)
    assert "campanha" in response.lower() or "facebook" in response.lower()

# Teste de processamento de input não-marketing
def test_process_user_input_non_marketing():
    question = "Qual a capital da França?"
    chat_history = []
    # Usando o fake do retriever e do LLM
    response = process_user_input(question, chat_history, llm_instance=FakeLLM(), retriever=fake_retriever)
    assert "desculpe" in response.lower()
