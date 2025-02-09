"use client"

import { useState } from "react"
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

export default function ChatAssistant() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input.trim(),
      role: 'user'
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // Send message to backend
      const response = await sendChatMessage(userMessage.content)
      
      // Add assistant's response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.error || response.message,
        role: 'assistant'
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, I'm having trouble connecting to the server.",
        role: 'assistant'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
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

        <CardContent className="h-[320px] overflow-y-auto p-3 space-y-3">
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
              {message.content}
            </div>
          ))}
          {isLoading && (
            <div className="flex items-center gap-2 text-sm text-gray-500 bg-white dark:bg-gray-800 p-2 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <Loader2 className="h-4 w-4 animate-spin" />
              Assistant is thinking...
            </div>
          )}
        </CardContent>

        <CardFooter className="border-t border-gray-200 dark:border-gray-700 p-3 bg-white dark:bg-gray-800">
          <form onSubmit={handleSubmit} className="flex w-full gap-2">
            <Input
              placeholder="Ask about the problem..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 text-sm bg-gray-50 dark:bg-gray-900 border-gray-200 dark:border-gray-700"
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

