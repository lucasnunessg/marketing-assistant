from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.llm.llm_setup import llm as default_llm
from app.validators.topic_validator import is_marketing_question, is_follow_up_question
from app.retrieve.text_retrieve import retrieve_marketing_info as default_retriever

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um especialista em marketing digital. Responda sempre com foco em vendas, redes sociais, tráfego e SEO."),
    ("user", "Quando surgiu o marketing digital?"),
    ("assistant", "O marketing digital começou a ganhar força no final dos anos 1990 com a popularização da internet e evoluiu com o avanço das redes sociais e plataformas de publicidade online."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("system", "[Contexto de apoio]: {context}"),
    ("human", "{question}")
])

def is_related_to_history(question: str, chat_history: list[dict]) -> bool:
    for entry in chat_history:
        if 'leads' in entry['content'].lower() and 'leads' in question.lower():
            return True
    return False

def ask_llm(
    question: str,
    docs: list[str],
    chat_history: list[dict],
    llm_instance=default_llm,
    retriever=default_retriever
) -> str:
    if any(word in question.lower() for word in ['bom dia', 'boa tarde', 'boa noite']):
        return "Bom dia! Como posso ajudar com seu marketing digital hoje?"
    elif any(word in question.lower() for word in ['oi', 'olá', 'ola']):
        return "Olá! Em que posso ajudar com marketing digital hoje?"

    context = "\n".join(docs)

    try:
        messages = chat_prompt.format_messages(
            chat_history=chat_history,
            question=question,
            context=context
        )

        response = llm_instance.invoke(messages)

        if is_related_to_history(question, chat_history):
            print("Pesquisando mais informações...")
            search_results = retriever(question)
            additional_info = "\n".join(search_results)
            response.content += "\n\nInformações adicionais encontradas:\n" + additional_info

        return response.content

    except Exception as e:
        print(f"Erro completo: {str(e)}")
        return f"Erro ao processar: {str(e)}"

def process_user_input(
    question: str,
    chat_history: list[dict],
    llm_instance=default_llm,
    retriever=default_retriever
) -> str:
    if not is_marketing_question(question) and not is_follow_up_question(question, chat_history):
        return "🤖 Desculpe, só consigo responder perguntas sobre marketing digital."

    if any(word in question.lower() for word in ['oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite']):
        chat_history = []

    docs = retriever(question)
    return ask_llm(question, docs, chat_history, llm_instance=llm_instance, retriever=retriever)
