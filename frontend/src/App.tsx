import { useState } from "react";
import "./App.css";
import { Message } from "./types";
import ReactMarkdown from "react-markdown";

function App() {
  const [question, setQuestion] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  const sendMessage = async () => {
    if (!question.trim()) return;

    const userMessage: Message = {
      role: "user",
      content: question,
    };

    const currentQuestion = question;

    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/chat-stream`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: currentQuestion,
            history: messages,
          }),
        }
      );

      if (!response.body) {
        throw new Error("No response body");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let assistantText = "";

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "",
        },
      ]);

      while (true) {
        const { value, done } =
          await reader.read();

        if (done) break;

        const chunk =
          decoder.decode(value);

        assistantText += chunk;

        setMessages((prev) => {
          const copy = [...prev];

          copy[copy.length - 1] = {
            role: "assistant",
            content: assistantText,
          };

          return copy;
        });
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (
    e: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="container">
      <h1>AI Stock Assistant</h1>

      <div className="chat-container">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.role}`}
          >
            <strong>
              {message.role === "user"
                ? "You"
                : "Assistant"}
            </strong>

            <ReactMarkdown>
              {message.content}
            </ReactMarkdown>
          </div>
        ))}

        {loading && (
          <div className="loading">
            Thinking...
          </div>
        )}
      </div>

      <div className="input-container">
        <input
          type="text"
          value={question}
          placeholder="Ask about stocks..."
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          onKeyDown={handleKeyDown}
        />

        <button onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;