"use client"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { MessageCircle, X, Send, Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"
import { sendChatMessage } from "@/lib/codeassist-chat-api"

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
}

interface ChatAssistantProps {
  problemContext: {
    userId?: string;
    concept?: string;
    complexity?: string;
    keywords?: string[];
    problemTitle?: string;
    problemDescription?: string;
    programmingLanguage?: string;
    currentCode?: string;
    testCases?: Array<{ input: any[]; output: any; }>;
    submissionResults?: {
      completed: boolean;
      passed: boolean;
      results: any[];
    };
  };
}

export default function ChatAssistant({ problemContext }: ChatAssistantProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const contentRef = useRef<HTMLDivElement>(null)

  // Function to scroll to bottom of chat
  const scrollToBottom = () => {
    if (contentRef.current) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input.trim(),
      role: 'user'
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    // Create a placeholder message for the assistant's response
    const assistantMessageId = (Date.now() + 1).toString()
    setMessages(prev => [...prev, {
      id: assistantMessageId,
      content: '',
      role: 'assistant'
    }])

    try {
      console.log('=== Sending Chat Message ===');
      console.log('Message:', userMessage.content);
      console.log('Context:', problemContext);

      await sendChatMessage(
        userMessage.content,
        {
          userId: problemContext.userId || 'guest',
          concept: problemContext.concept,
          complexity: problemContext.complexity,
          keywords: problemContext.keywords,
          problemTitle: problemContext.problemTitle,
          problemDescription: problemContext.problemDescription,
          programmingLanguage: problemContext.programmingLanguage,
          currentCode: problemContext.currentCode,
          testCases: problemContext.testCases,
          submissionResults: problemContext.submissionResults,
        },
        (chunk: string) => {
          // Update the assistant's message with the new chunk
          setMessages(prev => prev.map(msg => 
            msg.id === assistantMessageId
              ? { ...msg, content: msg.content + chunk }
              : msg
          ))
          scrollToBottom()
        }
      )
    } catch (error) {
      // Update the assistant's message with the error
      setMessages(prev => prev.map(msg => 
        msg.id === assistantMessageId
          ? { ...msg, content: "Sorry, I'm having trouble connecting to the server." }
          : msg
      ))
    } finally {
      setIsLoading(false)
      scrollToBottom()
    }
  }

  return (
    <>
      <Button
        onClick={() => setIsOpen(!isOpen)}
        className="h-10 w-10 rounded-full shadow-lg bg-blue-600 hover:bg-blue-700 text-white"
        size="icon"
      >
        {isOpen ? <X className="h-5 w-5" /> : <MessageCircle className="h-5 w-5" />}
      </Button>

      <Card
        className={cn(
          "absolute bottom-16 right-0 w-[380px] shadow-xl transition-all duration-200 ease-in-out",
          "bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-700",
          isOpen ? "translate-y-0 opacity-100" : "translate-y-4 opacity-0 pointer-events-none",
        )}
      >
        <CardHeader className="border-b border-gray-200 dark:border-gray-700 p-3 bg-white dark:bg-gray-800">
          <div className="flex items-center gap-2">
            <MessageCircle className="h-4 w-4 text-blue-600" />
            <h3 className="font-semibold text-sm">Problem Assistant</h3>
          </div>
        </CardHeader>

        <CardContent 
          ref={contentRef}
          className="h-[320px] overflow-y-auto p-3 space-y-3 scroll-smooth"
        >
          {messages.length === 0 && (
            <div className="text-sm text-gray-500 text-center py-4">
              Ask any questions about the problem!
            </div>
          )}
          
          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                "flex w-max max-w-[80%] rounded-lg px-3 py-2 text-sm",
                message.role === "user" 
                  ? "ml-auto bg-blue-600 text-white" 
                  : "bg-white dark:bg-gray-800 shadow-sm border border-gray-200 dark:border-gray-700",
              )}
            >
              {message.content || (
                <span className="animate-pulse">▋</span>
              )}
            </div>
          ))}
        </CardContent>

        <CardFooter className="border-t border-gray-200 dark:border-gray-700 p-3 bg-white dark:bg-gray-800">
          <form onSubmit={handleSubmit} className="flex w-full gap-2">
            <Input
              placeholder="Ask about the problem..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 text-sm bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-700"
              disabled={isLoading}
            />
            <Button 
              type="submit" 
              size="icon" 
              disabled={isLoading}
              className="bg-blue-600 hover:bg-blue-700 text-white shadow-sm"
            >
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </CardFooter>
      </Card>
    </>
  )
}

