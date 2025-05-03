def main():
    print("👋 Olá! Sou especialista em MARKETING DIGITAL.")
    print("Posso ajudar com:\n- Vendas online\n- Redes sociais\n- Publicidade\n- SEO\n")
    
    while True:
        try:
            user_input = input("Você: ").strip()
            
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("Até logo! 👋")
                break
                
            if not user_input:
                continue
                
            from app.validators.topic_validator import is_marketing_question
            if not is_marketing_question(user_input):
                print("🔒 Foco apenas em marketing digital. Posso ajudar com:")
                print("- Estratégias de vendas\n- Campanhas digitais\n- Gestão de redes sociais")
                continue
                
            from app.retrieve.text_retrieve import retrieve_marketing_info
            from app.chatbot.chatbot import ask_llm
            
            docs = retrieve_marketing_info(user_input)

            print("Processando resposta...")
            response = ask_llm(user_input, docs)
            print("\nAssistente:", response, "\n")
            
        except KeyboardInterrupt:
            print("\nOperação interrompida pelo usuário")
            break
        except Exception as e:
            print(f"⚠️ Erro: {str(e)}")

if __name__ == "__main__":
    main()