"use client"

import { Button } from "@/components/ui/button"
import ReactMarkdown from 'react-markdown'
import { Tag } from "lucide-react"
import ChatAssistant from "./chat-assistant"

interface ProblemDescriptionProps {
  title?: string;
  difficulty?: string;
  description?: string;
  concept?: string;
  onGenerateNewProblem: () => void;
  isGenerating?: boolean;
  tags?: string[];
  chatContext: {
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

export function ProblemDescription({ 
  title = "",
  difficulty = "Medium",
  description = "",
  concept = "",
  onGenerateNewProblem,
  isGenerating = false,
  tags = [],
  chatContext
}: ProblemDescriptionProps) {
  // Helper function to normalize difficulty
  const normalizeDifficulty = (diff: string): string => {
    const normalized = diff.toLowerCase();
    return normalized.charAt(0).toUpperCase() + normalized.slice(1);
  };

  return (
    <div className="relative h-full">
      <div className="h-full overflow-y-auto p-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">{title}</h1>
          <Button 
            onClick={onGenerateNewProblem}
            className="bg-blue-600 hover:bg-blue-700 text-white"
            disabled={isGenerating}
          >
            Solve Another
          </Button>
        </div>
        
        <div className="space-y-3">
          <div className="flex gap-2 items-center">
            {concept && (
              <div className="inline-block px-2 py-1 rounded text-blue-600 bg-blue-100 dark:bg-blue-900/30 text-sm">
                {concept}
              </div>
            )}
            <div className="inline-block px-2 py-1 rounded text-red-500 bg-red-100 dark:bg-red-900/30 text-sm">
              {normalizeDifficulty(difficulty)}
            </div>
          </div>

          {tags && tags.length > 0 && (
            <div className="flex flex-wrap gap-2 items-center">
              <Tag className="w-4 h-4 text-gray-500" />
              {tags.map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 text-xs rounded-full bg-gray-100 dark:bg-gray-800 
                            text-gray-600 dark:text-gray-300 hover:bg-gray-200 
                            dark:hover:bg-gray-700 transition-colors"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>

        <div className="prose prose-slate dark:prose-invert max-w-none mt-6">
          {description ? (
            <ReactMarkdown
              components={{
                h3: ({ children }) => (
                  <h3 className="text-xl font-semibold mt-6 mb-4">{children}</h3>
                ),
                p: ({ children }) => (
                  <p className="my-4">{children}</p>
                ),
                ul: ({ children }) => (
                  <ul className="list-disc pl-6 my-4">{children}</ul>
                ),
                li: ({ children }) => (
                  <li className="my-2">{children}</li>
                ),
                code: ({ node, inline, className, children, ...props }) => (
                  <code className={`${inline ? "bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded" : ""}`} {...props}>
                    {children}
                  </code>
                ),
                pre: ({ children }) => (
                  <pre className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 overflow-x-auto my-4 whitespace-pre-wrap break-words">
                    {children}
                  </pre>
                )
              }}
            >
              {description}
            </ReactMarkdown>
          ) : (
            <div className="text-gray-500 text-center py-8">
              Loading problem description...
            </div>
          )}
        </div>
      </div>

      {/* Position the ChatAssistant at the bottom of ProblemDescription */}
      <div className="absolute bottom-0 right-0 pb-4 pr-4">
        <ChatAssistant problemContext={chatContext} />
      </div>
    </div>
  )
}

