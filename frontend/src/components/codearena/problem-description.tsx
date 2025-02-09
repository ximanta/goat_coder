"use client"

import { Button } from "@/components/ui/button"
import ReactMarkdown from 'react-markdown'

interface ProblemDescriptionProps {
  title?: string;
  difficulty?: string;
  description?: string;
  onGenerateNewProblem: () => void;
  isGenerating?: boolean;
}

export function ProblemDescription({ 
  title = "10. Regular Expression Matching",
  difficulty = "Hard",
  description,
  onGenerateNewProblem,
  isGenerating = false 
}: ProblemDescriptionProps) {
  return (
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
      
      <div className="inline-block px-2 py-1 rounded text-red-500 bg-red-100 dark:bg-red-900/30 text-sm mb-4">
        {difficulty}
      </div>

      <div className="prose prose-slate dark:prose-invert max-w-none">
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
                <pre className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4 overflow-x-auto my-4">
                  {children}
                </pre>
              )
            }}
          >
            {description}
          </ReactMarkdown>
        ) : (
          <>
            <p>
              Given an input string <code>s</code> and a pattern <code>p</code>, implement regular expression matching with
              support for <code>.</code> and <code>*</code> where:
            </p>

            <ul>
              <li>
                <code>.</code> Matches any single character.
              </li>
              <li>
                <code>*</code> Matches zero or more of the preceding element.
              </li>
            </ul>

            <p>
              The matching should cover the <strong>entire</strong> input string (not partial).
            </p>

            <h2>Example 1:</h2>
            <pre>Input: s = "aa", p = "a" Output: false Explanation: "a" does not match the entire string "aa".</pre>
          </>
        )}
      </div>
    </div>
  )
}

