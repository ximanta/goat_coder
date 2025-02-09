"use client"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { MessageCircle, X, Send, Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"
import { sendChatMessage } from "@/lib/codeassist-chat-api"
import ReactMarkdown from 'react-markdown'

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
        className="h-10 w-10 rounded-full shadow-lg bg-blue-600 hover:bg-blue-700 text-white fixed bottom-4 left-4 z-50"
        size="icon"
        aria-label="Toggle Problem Mentor"
      >
        {isOpen ? <X className="h-5 w-5" /> : <MessageCircle className="h-5 w-5" />}
      </Button>

      <Card
        className={cn(
          "fixed inset-y-16 left-0 w-[500px] shadow-xl transition-all duration-300 ease-in-out z-40",
          "bg-gray-50/95 dark:bg-gray-900/95 border-2 border-blue-200 dark:border-blue-900 backdrop-blur-sm",
          isOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <CardHeader className="border-b border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MessageCircle className="h-5 w-5 text-blue-600" />
              <h3 className="font-semibold">Problem Mentor</h3>
            </div>
            <Button
              onClick={() => setIsOpen(false)}
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              aria-label="Close Problem Mentor"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </CardHeader>

        <CardContent 
          ref={contentRef}
          className="flex-1 overflow-y-auto p-4 space-y-4 h-[calc(100%-8rem)]"
        >
          {messages.length === 0 && (
            <div className="text-center py-8 space-y-2">
              <MessageCircle className="h-8 w-8 mx-auto text-blue-600/50" />
              <h4 className="font-semibold text-gray-600 dark:text-gray-400">
                Welcome to Problem Mentor!
              </h4>
              <p className="text-sm text-gray-500 dark:text-gray-500 max-w-sm mx-auto">
                Ask any questions about the problem. I'm here to guide you through the solution process.
              </p>
            </div>
          )}
          
          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                "flex rounded-lg px-4 py-2",
                message.role === "user" 
                  ? "ml-auto bg-blue-600 text-white max-w-[85%]" 
                  : "bg-white dark:bg-gray-800 shadow-sm border border-gray-200 dark:border-gray-700 max-w-[90%]",
              )}
            >
              {message.role === "user" ? (
                <div className="text-sm break-words whitespace-pre-wrap">
                  {message.content}
                </div>
              ) : message.content ? (
                <div className="prose prose-sm dark:prose-invert max-w-none break-words">
                  <ReactMarkdown
                    components={{
                      p: ({ children }) => (
                        <p className="my-1.5 whitespace-pre-wrap">{children}</p>
                      ),
                      ul: ({ children }) => (
                        <ul className="list-disc pl-4 my-2">{children}</ul>
                      ),
                      ol: ({ children }) => (
                        <ol className="list-decimal pl-4 my-2">{children}</ol>
                      ),
                      li: ({ children }) => (
                        <li className="my-1 whitespace-pre-wrap flex">
                          <span className="mr-2">{children}</span>
                        </li>
                      ),
                      code: ({ node, inline, className, children, ...props }) => (
                        <code 
                          className={cn(
                            "whitespace-pre-wrap break-all",
                            inline 
                              ? "bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded" 
                              : "block bg-gray-100 dark:bg-gray-800 p-3 rounded-md my-2"
                          )}
                          {...props}
                        >
                          {children}
                        </code>
                      ),
                    }}
                  >
                    {message.content}
                  </ReactMarkdown>
                </div>
              ) : (
                <span className="animate-pulse">▋</span>
              )}
            </div>
          ))}
        </CardContent>

        <CardFooter className="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-800">
          <form onSubmit={handleSubmit} className="flex w-full gap-2">
            <Input
              placeholder="Ask your mentor..."
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

