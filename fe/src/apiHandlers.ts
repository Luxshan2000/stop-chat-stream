import { sendMessage, abortRequest, QuestionPayload } from "./api";

export const handleSendMessage = async (
  payload: QuestionPayload,
  setAnswer: React.Dispatch<React.SetStateAction<string | null>>,
  setLoading: React.Dispatch<React.SetStateAction<boolean>>,
) => {
  setLoading(true);
  setAnswer("");

  try {
    const responseStream = await sendMessage(payload);

    const reader = responseStream.getReader();
    const decoder = new TextDecoder();
    let responseText = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      responseText += chunk;
      setAnswer((prev) => (prev || "") + chunk);
    }
  } catch (error) {
    console.error("Error during streaming:", error);
    setAnswer("Error occurred. Please try again.");
  } finally {
    setLoading(false);
  }
};

export const handleAbortRequest = async (request_id: string) => {
  try {
    await abortRequest(request_id);
  } catch (error) {
    console.error("Error during abort:", error);
  }
};
