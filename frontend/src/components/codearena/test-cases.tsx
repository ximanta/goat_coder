"use client"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { useState } from "react"

interface TestCase {
  id?: string;
  input: any[];
  output?: any;
}

interface TestCasesProps {
  testCases: TestCase[]
  results: Record<string, any>
  structure?: {
    input_structure: Array<{ Input_Field: string }>;
  }
}

export function TestCases({ testCases, results, structure }: TestCasesProps) {
  const [selectedTestCase, setSelectedTestCase] = useState(0)

  const renderParamValue = (value: any) => {
    if (Array.isArray(value)) {
      return `[${value.join(", ")}]`
    }
    if (typeof value === 'string') {
      return `"${value}"`
    }
    return String(value)
  }

  return (
    <Tabs defaultValue="testcase" className="w-full">
      <TabsList className="bg-background border-b rounded-none w-full justify-start h-12 p-0">
        <TabsTrigger value="testcase" className="data-[state=active]:bg-muted rounded-none h-full px-4">
          Testcase
        </TabsTrigger>
        <TabsTrigger value="result" className="data-[state=active]:bg-muted rounded-none h-full px-4">
          Test Result
        </TabsTrigger>
      </TabsList>
      <TabsContent value="testcase" className="p-0 border-0">
        <Card className="border-0 shadow-none">
          <CardContent className="p-4">
            <div className="flex flex-wrap gap-2 mb-4">
              {testCases.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedTestCase(index)}
                  className={`px-3 py-1 rounded-full text-sm ${
                    selectedTestCase === index
                      ? "bg-blue-600 text-white"
                      : "bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700"
                  }`}
                >
                  Test Case {index + 1}
                </button>
              ))}
            </div>

            {testCases[selectedTestCase] && structure?.input_structure && (
              <div className="space-y-4">
                {structure.input_structure.map((param, index) => (
                  <div key={index} className="space-y-1">
                    <Label className="text-sm font-medium">
                      Param {index + 1} - {param.Input_Field.split(" ")[1]}
                    </Label>
                    <div className="p-2 rounded bg-muted font-mono text-sm">
                      {renderParamValue(testCases[selectedTestCase].input[index])}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </TabsContent>
      <TabsContent value="result" className="p-0 border-0">
        <Card className="border-0 shadow-none">
          <CardContent className="p-4">
            <pre className="whitespace-pre-wrap font-mono text-sm">{JSON.stringify(results, null, 2)}</pre>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  )
}

