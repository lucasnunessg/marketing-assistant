from langchain_core.prompts import ChatPromptTemplate
from app.chatbot.chatbot import llm

MARKETING_KEYWORDS = {
    'marketing', 'mkt', 'vendas', 'publicidade', 'anúncio', 
    'redes sociais', 'instagram', 'facebook', 'linkedin',
    'campanha', 'conversão', 'lead', 'tráfego', 'seo', 'branding'
}

def is_marketing_question(question: str) -> bool:
    question_lower = question.lower()
    if not any(keyword in question_lower for keyword in MARKETING_KEYWORDS):
        return False

    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        ANALISE SE A PERGUNTA É SOBRE MARKETING DIGITAL.
        Responda APENAS 'SIM' ou 'NÃO'.

        Critérios de MARKETING:
        - Estratégias de vendas ou divulgação
        - Gestão de mídias sociais
        - Publicidade e propaganda
        - Métricas e análise de desempenho
        - Conteúdo para negócios

        Pergunta: {question}
        Resposta:""")
    ])
    
    try:
        messages = prompt.format_messages(question=question)
        response = llm.invoke(messages)
        return "SIM" in response.content.upper()
    except Exception:
        return False
