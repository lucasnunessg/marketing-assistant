from fastapi.testclient import TestClient
from app.api.main import app 

class FakeLLM:
    def invoke(self, messages):
        return type("Response", (), {"content": "Resposta fake do LLM"})()

def fake_retriever(question):
    return ["Fake contexto 1", "Fake contexto 2"]

def override_llm():
    return FakeLLM()

def override_retriever():
    return fake_retriever

def test_chat_endpoint():
    client = TestClient(app)
    
    app.dependency_overrides[FakeLLM] = override_llm
    app.dependency_overrides[fake_retriever] = override_retriever
    
    payload = {
        "question": "Como melhorar meu engajamento no Instagram?",
        "docs": [],
        "chat_history": []
    }
    
    response = client.post("/chat", json=payload)

    assert response.status_code == 200
    assert "response" in response.json()

    app.dependency_overrides.clear()
