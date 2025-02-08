"use client"

import { useState, useEffect } from "react"
import { ProblemDescription } from "@/components/codearena/problem-description"
import { CodeEditor } from "@/components/codearena/code-editor"
import { useTheme } from "next-themes"
import { submitCode } from "@/services/code-submission"
import { generateProblem } from "@/lib/get_problem_api"
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels"
import { ProblemResponse } from "@/lib/get_problem_api"
import { Loader2, ArrowLeft } from "lucide-react"

export interface CodeArenaProps {
  category?: string;
  onBack?: () => void;
}

interface TestCaseResult {
  test_case_index: number;
  passed: boolean;
  stdout?: string;
  stderr?: string;
  compile_output?: string;
  expected_output?: string;
  status: {
    id: number;
    description: string;
  };
}

export default function CodeArena({ category, onBack }: CodeArenaProps) {
  const [code, setCode] = useState("")
  const [language, setLanguage] = useState("4")
  const [status, setStatus] = useState("")
  const [loading, setLoading] = useState(true)
  const [problem, setProblem] = useState<{
    title: string;
    difficulty: string;
    description: string;
    testCases: { input: any[]; output: any; }[];
    structure: {
      problem_name: string;
      function_name: string;
      input_structure: Array<{ Input_Field: string }>;
      output_structure: { Output_Field: string };
    };
    javaBoilerplate: string;
    pythonBoilerplate: string;
  }>({
    title: "10. Regular Expression Matching",
    difficulty: "Hard",
    description: "",
    testCases: [],
    structure: {
      problem_name: "",
      function_name: "",
      input_structure: [],
      output_structure: { Output_Field: "" }
    },
    javaBoilerplate: "",
    pythonBoilerplate: ""
  })
  const { theme } = useTheme()
  const [testResults, setTestResults] = useState<{
    completed: boolean;
    passed: boolean;
    results: TestCaseResult[];
  }>({
    completed: false,
    passed: false,
    results: []
  });

  useEffect(() => {
    handleGenerateNewProblem()
  }, [category])

  const handleGenerateNewProblem = async () => {
    try {
      setLoading(true)
      const complexities = ["EASY", "MEDIUM", "HARD"]
      const randomComplexity = complexities[Math.floor(Math.random() * complexities.length)]
      const newProblem = await generateProblem(category, randomComplexity)
      setProblem({
        title: newProblem.problem_title,
        difficulty: newProblem.difficulty,
        description: newProblem.problem_statement,
        testCases: newProblem.test_cases,
        structure: newProblem.structure,
        javaBoilerplate: newProblem.java_boilerplate,
        pythonBoilerplate: newProblem.python_boilerplate
      })
      setCode("")
      setStatus("")
    } catch (error) {
      console.error("Failed to generate new problem:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (result: { status: { description: string; results: any[] } }) => {
    try {
      console.log('=== Submit Result ===');
      console.log('Result:', result);
      
      if (result?.status) {
        setTestResults({
          completed: true,
          passed: result.status.results.every(r => r.passed),
          results: result.status.results
        });
        setStatus(result.status.description);
      }
    } catch (error) {
      console.error('Error handling submit:', error);
      setStatus(error instanceof Error ? error.message : 'Submission failed');
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <Loader2 className="h-12 w-12 animate-spin text-indigo-600" />
        <p className="mt-4 text-lg text-gray-600">Loading your coding challenge...</p>
      </div>
    )
  }

  console.log('=== CodeArena Render ===');
  console.log('Problem structure:', problem?.structure);

  return (
    <div className="relative min-h-screen">
      <div className="fixed top-0 left-0 right-0 h-16 bg-white border-b border-border z-10 px-4 flex items-center">
        <button 
          onClick={onBack}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-50 p-2 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Back</span>
        </button>
      </div>

      <PanelGroup direction="horizontal" className="min-h-screen pt-16">
        <Panel defaultSize={40} minSize={30}>
          <div className="h-full overflow-hidden border-r border-border">
            <ProblemDescription
              title={problem.title}
              difficulty={problem.difficulty}
              description={problem.description}
              onGenerateNewProblem={handleGenerateNewProblem}
            />
          </div>
        </Panel>

        <PanelResizeHandle className="w-2 bg-border hover:bg-muted/50 cursor-col-resize" />

        <Panel defaultSize={60} minSize={40}>
          <div className="h-full">
            <CodeEditor
              code={code}
              language={language}
              onCodeChange={setCode}
              onLanguageChange={setLanguage}
              onSubmit={handleSubmit}
              status={status}
              structure={problem.structure}
              testCases={problem.testCases}
              javaBoilerplate={problem.javaBoilerplate}
              pythonBoilerplate={problem.pythonBoilerplate}
              testResults={testResults}
            />
          </div>
        </Panel>
      </PanelGroup>
    </div>
  )
}

