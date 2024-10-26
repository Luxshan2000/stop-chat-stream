export interface QuestionPayload {
  request_id: string;
  model: string;
  messages: { role: string; content: string }[];
  stream: boolean;
}

export async function sendMessage(
  payload: QuestionPayload,
): Promise<ReadableStream<Uint8Array>> {
  const response = await fetch("http://localhost:8000/chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.body) {
    throw new Error("ReadableStream not supported in this environment.");
  }

  return response.body;
}

export async function abortRequest(request_id: string): Promise<void> {
  await fetch("http://localhost:8000/abort/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ request_id }),
  });
}
