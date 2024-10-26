import React, { useState } from "react";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";

const Chat: React.FC = () => {
  const [question, setQuestion] = useState<{
    question: string;
    request_id: string;
  }>();
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [abort, setAbort] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setAnswer("");
    setLoading(true);
    // setAbort(false);

    try {
      const response = await fetch("http://localhost:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          request_id: uuidv4().toString(),
          model: "gpt-3.5-turbo-0125",
          messages: [{ role: "user", content: "hello" }],
          stream: true,
        }),
        // signal: abortController.current.signal,
      });

      if (!response.body)
        throw new Error("ReadableStream not supported in this environment.");

      const reader = response.body.getReader();
      let responseText = "";
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done || abort) break;

        const chunk = decoder.decode(value, { stream: true });
        responseText += chunk;
        console.log(chunk);

        setAnswer((prev) => prev + chunk);
      }
    } catch (error) {
      if (abort) {
        console.log("Streaming request was aborted.");
      } else {
        console.error("Error during streaming:", error);
      }
    } finally {
      setLoading(false);
    }
  };
  return (
    <div>
      <h1>Chat with AI</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question?.question}
          onChange={(e) =>
            setQuestion({ question: e.target.value, request_id: uuidv4() })
          }
          placeholder="Ask your question..."
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Send"}
        </button>
      </form>
      {answer && (
        <div>
          <h2>Answer:</h2>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default Chat;
