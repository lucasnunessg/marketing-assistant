import pytest
from app.validators.topic_validator import is_marketing_question, is_follow_up_question

# Teste de validação se a pergunta é sobre marketing
@pytest.mark.parametrize("question,expected", [
    ("Como melhorar o SEO do meu site?", True),
    ("Qual o preço do dólar?", False),
])
def test_is_marketing_question(question, expected):
    assert is_marketing_question(question) == expected

# Teste de pergunta de follow-up verdadeira
def test_is_follow_up_question_true():
    question = "Como posso melhorar isso?"
    chat_history = [
        {"role": "user", "content": "Quero mais leads pelo Instagram"}
    ]
    assert is_follow_up_question(question, chat_history) is True

# Teste de pergunta de follow-up falsa
def test_is_follow_up_question_false():
    question = "Como está o clima?"
    chat_history = [{"role": "user", "content": "Hoje está calor"}]
    assert is_follow_up_question(question, chat_history) is False
