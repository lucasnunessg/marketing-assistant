import { useState, useEffect, ChangeEvent, useRef } from "react";
import VoiceInput from "./VoiceInput";
import "../index.css";

interface Message {
  role: "user" | "assistant";
  content: string;
}

function ChatComponent() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messageEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const fetchWelcomeMessage = async () => {
      try {
        const response = await fetch("http://localhost:8000/info");
        const data = await response.json();
        setMessages([{ role: "assistant", content: data.response }]);
      } catch {
        setMessages([
          {
            role: "assistant",
            content: "Erro ao carregar a mensagem inicial.",
          },
        ]);
      }
    };
    fetchWelcomeMessage();
  }, []);

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleUserInput = (e: ChangeEvent<HTMLInputElement>) => {
    setUserInput(e.target.value);
  };

  const handleSendMessage = async () => {
    if (!userInput.trim()) return;

    const newMessage: Message = { role: "user", content: userInput };
    setMessages((prev) => [...prev, newMessage]);
    setUserInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: newMessage.content,
          docs: [],
          chat_history: messages,
        }),
      });
      const data = await response.json();
      console.log(data.response);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Erro ao processar a pergunta." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="header">
        <div className="logo-container">
          <img
            src="https://intellux.com/Intellux_Simbolo_Verde_RGB.svg"
            alt="Logo"
            className="logo"
          />
          <span className="logo-text">intellux</span>
        </div>
        <h1>Chat de Marketing Digital</h1>
      </div>

      <div className="messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${
              msg.role === "assistant" ? "assistant" : "user"
            }`}
          >
            {msg.content
              .split(".")
              .map((frase, i) =>
                frase.trim() ? <p key={i}>{frase.trim()}.</p> : null
              )}
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <p>
              <span className="spinner" /> Digitando...
            </p>
          </div>
        )}
        <div ref={messageEndRef} />
      </div>

      <div className="input-container">
        <input
          type="text"
          placeholder="Digite sua mensagem..."
          value={userInput}
          onChange={handleUserInput}
          disabled={loading}
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
        />
        <VoiceInput onText={(text) => setUserInput(text)} />
        <button
          onClick={handleSendMessage}
          disabled={loading || !userInput.trim()}
        >
          {loading ? "Enviando..." : "Enviar"}
        </button>
      </div>
      <div className="footer">
        <p>© Teste Técnico Intellux - Lucas Nunes - 05/2025</p>
      </div>
    </div>
    
  );
}

export default ChatComponent;
