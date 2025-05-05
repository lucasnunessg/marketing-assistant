from app.chatbot.chatbot import process_user_input

class FakeLLM:
    def invoke(self, messages):
        return type("Response", (), {"content": "Resposta fake do LLM"})()

def fake_retriever(question):
    return ["Fake contexto 1", "Fake contexto 2"]

def test_process_user_input_marketing():
    question = "Como criar uma campanha no Facebook Ads?"
    chat_history = []
    response = process_user_input(question, chat_history, llm_instance=FakeLLM(), retriever=fake_retriever)
    assert isinstance(response, str)
    assert response == "Resposta fake do LLM" 

def test_process_user_input_non_marketing():
    question = "Qual a capital da França?"
    chat_history = []
    response = process_user_input(question, chat_history, llm_instance=FakeLLM(), retriever=fake_retriever)
    assert "desculpe" in response.lower()
