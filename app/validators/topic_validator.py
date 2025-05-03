from langchain_core.prompts import ChatPromptTemplate
from app.llm.llm_setup import llm


MARKETING_KEYWORDS = {
    'marketing', 'mkt', 'vendas', 'publicidade', 'anúncio', 
    'redes sociais', 'instagram', 'facebook', 'linkedin',
    'campanha', 'conversão', 'lead', 'tráfego', 'seo', 'branding'
}



def is_follow_up_question(question: str, chat_history: list[dict]) -> bool:
    if not chat_history:
        return False
    
    last_interactions = chat_history[-4:] if len(chat_history) >= 4 else chat_history
    
    has_marketing_context = any(
        any(keyword in interaction['content'].lower() for keyword in MARKETING_KEYWORDS)
        for interaction in last_interactions
        if interaction['role'] == 'user'
    )
    
    continuation_words = {'isso', 'como', 'porque', 'por que', 'explique', 'detalhe', 'mais', 'o que é'}
    question_words = set(question.lower().split())
    
    return has_marketing_context and bool(continuation_words & question_words)

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
    except Exception as e:
        print(f"Erro ao invocar o modelo: {str(e)}")
        return False
    


