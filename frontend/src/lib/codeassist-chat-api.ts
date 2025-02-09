interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatResponse {
  message: string;
  error?: string;
}

export async function sendChatMessage(message: string): Promise<ChatResponse> {
  try {
    const response = await fetch("http://localhost:8000/codeassist/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Chat API Error:', errorText);
      throw new Error(`Failed to send message: ${errorText}`);
    }

    const data = await response.json();
    return {
      message: data.response,
    };
  } catch (error) {
    console.error('Chat API Error:', error);
    return {
      message: "Sorry, I'm having trouble connecting to the server.",
      error: error instanceof Error ? error.message : 'Unknown error occurred',
    };
  }
} 