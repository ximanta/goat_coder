"use client"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { cn } from "@/lib/utils"
import { Loader2 } from "lucide-react"
import { useState } from "react"

interface TestCase {
  input: any[]
  output: any
}

interface TestCaseResult {
  test_case_index: number
  passed: boolean
  stdout?: string
  stderr?: string
  compile_output?: string
  expected_output?: string
  status: {
    id: number
    description: string
  }
}

interface TestCasesProps {
  testCases?: TestCase[]
  results?: {
    completed: boolean
    passed: boolean
    results: TestCaseResult[]
  }
  structure?: {
    input_structure: Array<{ Input_Field: string }>
    output_structure: { Output_Field: string }
  }
  isGenerating?: boolean
}

export function TestCases({ testCases = [], results, structure, isGenerating }: TestCasesProps) {
  const renderTestResult = (result: TestCaseResult) => {
    const hasError = result.compile_output || result.stderr;
    const statusColor = result.passed ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200';
    const textColor = result.passed ? 'text-green-800' : 'text-red-800';

    return (
      <div className={`p-4 border rounded-lg mb-4 ${statusColor}`}>
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-medium">Test Case {result.test_case_index + 1}</h3>
          <span className={`px-2 py-1 rounded-full text-sm font-medium ${textColor}`}>
            {result.passed ? 'Passed' : 'Failed'}
          </span>
        </div>
        
        <div className="space-y-3 text-sm">
          {hasError && (
            <div className="text-red-600">
              {result.compile_output && (
                <div className="mb-2">
                  <div className="font-medium">Compilation Error:</div>
                  <pre className="mt-1 p-2 bg-red-50 rounded whitespace-pre-wrap">{result.compile_output}</pre>
                </div>
              )}
              {result.stderr && (
                <div className="mb-2">
                  <div className="font-medium">Runtime Error:</div>
                  <pre className="mt-1 p-2 bg-red-50 rounded whitespace-pre-wrap">{result.stderr}</pre>
                </div>
              )}
            </div>
          )}
          
          <div>
            <div className="font-medium">Your Output:</div>
            <pre className="mt-1 p-2 bg-gray-50 rounded whitespace-pre-wrap">{result.stdout || '(no output)'}</pre>
          </div>
          
          <div>
            <div className="font-medium">Expected Output:</div>
            <pre className="mt-1 p-2 bg-gray-50 rounded whitespace-pre-wrap">{result.expected_output}</pre>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="h-full">
      <Tabs defaultValue="test1" className="h-full flex flex-col">
        <TabsList className="grid w-full grid-cols-4">
          {testCases.map((_, index) => (
            <TabsTrigger
              key={`test${index + 1}`}
              value={`test${index + 1}`}
              className="text-sm"
            >
              Test {index + 1}
            </TabsTrigger>
          ))}
          <TabsTrigger value="results" className="text-sm">
            Results
          </TabsTrigger>
        </TabsList>

        {testCases.map((testCase, index) => (
          <TabsContent
            key={`test${index + 1}`}
            value={`test${index + 1}`}
            className="flex-1 overflow-auto"
          >
            <div className="p-4 space-y-4 rounded-lg bg-white">
              <div>
                <h3 className="font-medium mb-2">Input:</h3>
                <pre className="p-2 bg-gray-50 rounded text-sm">
                  {JSON.stringify(testCase.input, null, 2)}
                </pre>
              </div>
              <div>
                <h3 className="font-medium mb-2">Expected Output:</h3>
                <pre className="p-2 bg-gray-50 rounded text-sm">
                  {JSON.stringify(testCase.output, null, 2)}
                </pre>
              </div>
            </div>
          </TabsContent>
        ))}

        <TabsContent value="results" className="flex-1 overflow-auto">
          {isGenerating ? (
            <div className="h-full flex items-center justify-center">
              <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
            </div>
          ) : results ? (
            <div className="p-4 space-y-4">
              <div className={`p-4 rounded-lg ${
                results.passed ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
              }`}>
                <h3 className="font-medium mb-2">Overall Results</h3>
                <div className="space-y-1 text-sm">
                  <p>Status: {results.completed ? 'Completed' : 'Processing'}</p>
                  <p>Total Tests: {results.results.length}</p>
                  <p>Passed: {results.results.filter(r => r.passed).length}</p>
                  <p>Failed: {results.results.filter(r => !r.passed).length}</p>
                </div>
              </div>
              
              <div className="space-y-4">
                {results.results.map((result, index) => (
                  <div key={index}>
                    {renderTestResult(result)}
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center text-gray-500">
              Run your code to see results
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}

