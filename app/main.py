from app.validators.topic_validator import is_marketing_question, is_follow_up_question
from app.retrieve.text_retrieve import retrieve_marketing_info
from app.chatbot.chatbot import ask_llm

def is_greeting(text: str) -> bool:
    greetings = ['bom dia', 'boa tarde', 'boa noite', 'oi', 'olá', 'ola']
    return any(word in text.lower() for word in greetings)

def main():
    print("👋 Olá! Sou especialista em MARKETING DIGITAL.")
    print("Posso ajudar com:\n- Vendas online\n- Redes sociais\n- Publicidade\n- SEO\n")
    
    chat_history = []
    last_marketing_topic = None

    while True:
        try:
            user_input = input("Você: ").strip()
 

            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("Até logo! 👋")
                break
                
            if not user_input:
                continue

            if is_greeting(user_input):
                response = ask_llm(user_input, [], chat_history)
                print("\nAssistente:", response, "\n")
                chat_history.append({"role": "user", "content": user_input})
                chat_history.append({"role": "assistant", "content": response})
                continue  

            is_follow_up = is_follow_up_question(user_input, chat_history) if last_marketing_topic else False
            
            if not is_marketing_question(user_input) and not is_follow_up:
                print("Eu não fui programado para responder sobre este assunto, mas podemos retomar nossa conversa:")
                continue
                
            docs = retrieve_marketing_info(user_input)
            print("Processando resposta...")
            response = ask_llm(user_input, docs, chat_history)
            print("\nAssistente:", response, "\n")

            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": response})
            
            if is_marketing_question(user_input) or is_follow_up:
                last_marketing_topic = user_input

        except KeyboardInterrupt:
            print("\nOperação interrompida pelo usuário")
            break
        except Exception as e:
            print(f"⚠️ Erro: {str(e)}")

if __name__ == "__main__":
    main()