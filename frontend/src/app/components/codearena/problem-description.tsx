"use client"

import { Button } from "@/app/components/ui/button"
import ReactMarkdown from 'react-markdown'
import { Tag, ArrowRight } from "lucide-react"
import ChatAssistant from "./chat-assistant"
import { CommonCodeArena } from "./common-code-arena"
import { useState } from "react"

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
  const [resetTrigger, setResetTrigger] = useState(0);

  const handleGenerateNewProblem = () => {
    setResetTrigger(prev => prev + 1); // Increment reset trigger
    onGenerateNewProblem();
  };

  // Helper function to normalize difficulty
  const normalizeDifficulty = (diff: string): string => {
    const normalized = diff.toLowerCase();
    return normalized.charAt(0).toUpperCase() + normalized.slice(1);
  };

  // Helper function to get difficulty styles
  const getDifficultyStyles = (diff: string): string => {
    const normalized = diff.toLowerCase();
    switch (normalized) {
      case 'easy':
        return 'bg-green-100 text-green-700'; // Light green background, darker green text
      case 'medium':
        return 'bg-green-200 text-green-800'; // Medium green background, darker green text
      case 'hard':
        return 'bg-green-300 text-green-900'; // Darker green background, darkest green text
      default:
        return 'bg-green-100 text-green-700';
    }
  };

  return (
    <div className="relative h-full flex flex-col bg-white">
      {/* Main content - scrollable area */}
      <div className="flex-1 overflow-y-auto pb-20 custom-scrollbar bg-white"> {/* Added custom-scrollbar class */}
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-2xl font-bold">{title}</h1>
            <Button 
              onClick={handleGenerateNewProblem}
              className="bg-blue-50 hover:bg-blue-100 text-blue-600 border-none shadow-none gap-2 transition-colors"
              disabled={isGenerating}
            >
              Next Challenge
              <ArrowRight className="h-4 w-4" />
            </Button>
          </div>
          
          <div className="space-y-3">
            <div className="flex gap-2 items-center">
              {concept && (
                <div className="inline-block px-2 py-1 rounded text-blue-600 bg-blue-100 dark:bg-blue-900/30 text-sm">
                  {concept}
                </div>
              )}
              <div className={`inline-block px-2 py-1 rounded text-sm ${getDifficultyStyles(difficulty)}`}>
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
      </div>

      {/* Fixed position buttons container */}
      <div className="absolute bottom-4 right-4 flex flex-col gap-2 z-10">
        <ChatAssistant 
          problemContext={chatContext} 
          resetTrigger={resetTrigger}
        />
        <CommonCodeArena />
      </div>

      {/* Add a gradient overlay to improve visibility of buttons over text */}
      <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-white to-transparent pointer-events-none" />
    </div>
  )
}

