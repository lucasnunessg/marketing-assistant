from retrieve.text_retrieve import retrieve_marketing_info
from chatbot.chatbot import ask_llm


def main():
    print("👋 Olá! Sou seu assistente de marketing. Como posso ajudar?")
    print("Digite 'sair' a qualquer momento para encerrar.\n")
    
    while True:
        user_input = input("Você: ").strip()
        
        if user_input.lower() in ['sair', 'exit', 'quit']:
            print("Até logo! 👋")
            break
            
        if not user_input:
            print("Por favor, digite sua pergunta sobre marketing.")
            continue
            
        try:
            docs = retrieve_marketing_info(user_input)
            
            response = ask_llm(user_input, docs)
            
            print("\nAssistente:", response, "\n")
            
        except Exception as e:
            print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()