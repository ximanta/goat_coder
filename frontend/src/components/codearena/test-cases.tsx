"use client"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { cn } from "@/lib/utils"
import { Loader2 } from "lucide-react"

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
  testCases: TestCase[]
  results?: {
    submitted: boolean
    completed: boolean
    passed: boolean
    results: TestCaseResult[]
  }
  structure: any
  isGenerating?: boolean
}

export function TestCases({ testCases, results, structure, isGenerating = false }: TestCasesProps) {
  console.log('TestCases render:', { testCases, results });
  
  return (
    <Tabs defaultValue="test-result" className="w-full">
      <div className="border rounded-lg p-2 bg-background">
        <TabsList className="grid w-full" style={{
          gridTemplateColumns: `repeat(${testCases.length}, 1fr) 1.5fr`
        }}>
          {testCases.map((_, index) => {
            const result = results?.results?.find(r => r.test_case_index === index);
            console.log(`Test ${index} result:`, result);
            return (
              <TabsTrigger 
                key={index} 
                value={`test-${index}`}
                className={cn(
                  "border-r last:border-r-0",
                  result?.passed && "bg-green-500 text-white hover:bg-green-600",
                  result?.passed === false && "bg-red-500 text-white hover:bg-red-600"
                )}
              >
                Test {index + 1}
              </TabsTrigger>
            );
          })}
          <TabsTrigger 
            value="test-result"
            className={cn(
              "border-l ml-2 bg-gray-100 hover:bg-gray-200",
              results?.submitted && results.passed && "bg-green-100 hover:bg-green-200",
              results?.submitted && !results?.passed && "bg-red-100 hover:bg-red-200"
            )}
          >
            Submission Results
          </TabsTrigger>
        </TabsList>
      </div>

      <TabsContent value="test-result" className="p-4">
        {!results?.submitted ? (
          <p className="text-gray-600">Please submit your code to view results</p>
        ) : results ? (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Overall Results</h3>
            <div className="space-y-2">
              <p>Status: {results.completed ? "Completed" : "Running..."}</p>
              <p className={cn(
                "font-medium",
                results.passed ? "text-green-600" : "text-red-600"
              )}>
                {results.passed ? "All Tests Passed!" : "Some Tests Failed"}
              </p>
              <p>Total Tests: {testCases.length}</p>
              <p>Passed: {results.results?.filter(r => r.passed)?.length || 0}</p>
              <p>Failed: {results.results?.filter(r => !r.passed)?.length || 0}</p>
            </div>
          </div>
        ) : (
          <p>Run your code to see results</p>
        )}
      </TabsContent>

      {testCases.map((testCase, index) => (
        <TabsContent key={index} value={`test-${index}`} className="p-4">
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold mb-2">Input:</h3>
              <pre className="bg-gray-100 p-2 rounded">
                {testCase.input.map((input, i) => (
                  <div key={i}>{JSON.stringify(input)}</div>
                ))}
              </pre>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-2">Expected Output:</h3>
              <pre className="bg-gray-100 p-2 rounded">
                {JSON.stringify(testCase.output)}
              </pre>
            </div>

            {results?.results?.[index] && (
              <>
                <div>
                  <h3 className="text-lg font-semibold mb-2">Your Output:</h3>
                  <pre className="bg-gray-100 p-2 rounded">
                    {results.results[index].stdout?.trim() || "No output"}
                  </pre>
                </div>

                {results.results[index].stderr && (
                  <div>
                    <h3 className="text-lg font-semibold mb-2 text-red-600">Errors:</h3>
                    <pre className="bg-red-50 text-red-600 p-2 rounded">
                      {results.results[index].stderr}
                    </pre>
                  </div>
                )}

                <div className={cn(
                  "p-4 rounded-lg",
                  results.results[index].passed ? "bg-green-50" : "bg-red-50"
                )}>
                  <p className={cn(
                    "font-semibold",
                    results.results[index].passed ? "text-green-600" : "text-red-600"
                  )}>
                    Status: {results.results[index].status.description}
                  </p>
                </div>
              </>
            )}
          </div>
        </TabsContent>
      ))}
    </Tabs>
  )
}

