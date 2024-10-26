import React, { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { handleSendMessage, handleAbortRequest } from "./apiHandlers";

interface Question {
  question: string;
  request_id: string;
}

const Chat: React.FC = () => {
  const [question, setQuestion] = useState<Question>({
    question: "",
    request_id: "",
  });
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSend = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();

    const updatedQuestion = {
      question: question.question,
      request_id: question.request_id || uuidv4(),
    };
    setQuestion(updatedQuestion);

    await handleSendMessage(
      {
        request_id: updatedQuestion.request_id,
        model: "gpt-3.5-turbo-0125",
        messages: [{ role: "user", content: updatedQuestion.question }],
        stream: true,
      },
      setAnswer,
      setLoading,
    );
  };

  const handleAbort = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    await handleAbortRequest(question.request_id);
  };

  return (
    <div className="chat-container">
      <h1 className="chat-title">Chat with AI</h1>
      <form className="chat-form">
        <input
          type="text"
          value={question.question}
          onChange={(e) =>
            setQuestion({ question: e.target.value, request_id: uuidv4() })
          }
          placeholder="Ask your question..."
          required
          className="chat-input"
          disabled={loading}
        />
        {!loading ? (
          <button onClick={handleSend} className="chat-button">
            Send
          </button>
        ) : (
          <button onClick={handleAbort} className="chat-button">
            Stop
          </button>
        )}
      </form>
      {answer && (
        <div className="chat-answer">
          <p className="answer-text">{answer}</p>
        </div>
      )}
    </div>
  );
};

export default Chat;
