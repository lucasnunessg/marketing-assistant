import { useState, useRef } from "react";
import { FaMicrophone, FaMicrophoneSlash } from "react-icons/fa";
import "../index.css";



interface VoiceInputProps {
  onText: (transcript: string) => void;
}

const VoiceInput = ({ onText }: VoiceInputProps) => {
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  const getSpeechRecognition = () => {
    return window.SpeechRecognition || window.webkitSpeechRecognition;
  };

  const startListening = () => {
    const Recognition = getSpeechRecognition();
    if (!Recognition) {
      alert("Seu navegador não suporta reconhecimento de voz.");
      return;
    }

    const recognition = new Recognition();
    recognition.lang = "pt-BR";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0][0].transcript;
      onText(transcript);
    };

    recognition.onend = () => setListening(false);
    recognition.onerror = (event) => {
      console.error("Erro no reconhecimento de voz:", event);
      setListening(false);
    };

    recognition.start();
    recognitionRef.current = recognition;
    setListening(true);
  };

  const stopListening = () => {
    recognitionRef.current?.stop();
    setListening(false);
  };

  return (
<button
  onClick={listening ? stopListening : startListening}
  className={`voice-button ${listening ? 'listening' : ''}`}
  aria-label={listening ? "Parar gravação" : "Iniciar gravação"}
>
  {listening ? <FaMicrophoneSlash /> : <FaMicrophone />}
</button>
  
  
  );
};

export default VoiceInput;