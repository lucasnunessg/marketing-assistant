from app.retrieve.text_retrieve import retrieve_marketing_info

def fake_retriever(question):
    return ["Fake contexto 1", "Fake contexto 2"]

def test_retrieve_marketing_info():
    results = fake_retriever("como gerar leads")
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(item, str) for item in results)
