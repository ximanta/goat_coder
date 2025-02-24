interface ChatContext {
  userId: string;
  concept?: string;
  complexity?: string;
  keywords?: string[];
  problemTitle?: string;
  problemDescription?: string;
  programmingLanguage?: string;
  currentCode?: string;
  testCases?: Array<{ input: string[]; output: string; }>;
  submissionResults?: {
    completed: boolean;
    passed: boolean;
    results: string[];
  };
}
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;
export async function sendChatMessage(
  message: string, 
  context: ChatContext,
  onChunk: (chunk: string) => void
): Promise<void> {
  try {
    console.log('=== Chat API Call ===');
    console.log('Sending to backend:', { message, context });

    const response = await fetch(`${API_BASE_URL}/codeassist/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        context
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Chat API Error:', errorText);
      throw new Error(`Failed to send message: ${errorText}`);
    }

    if (!response.body) {
      throw new Error('No response body received');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      onChunk(chunk);
    }

  } catch (error) {
    console.error('Chat API Error:', error);
    throw error;
  }
} 