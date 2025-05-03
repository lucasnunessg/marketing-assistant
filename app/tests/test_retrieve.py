from app.retrieve.text_retrieve import retrieve_marketing_info

# Fake para o retriever
def fake_retriever(question):
    return ["Fake contexto 1", "Fake contexto 2"]

# Teste do retrieve_marketing_info com fake
def test_retrieve_marketing_info():
    # Usando o fake do retriever
    results = fake_retriever("como gerar leads")
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(item, str) for item in results)
