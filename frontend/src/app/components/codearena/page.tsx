"use client"

import { useState, useEffect } from "react"
import { ProblemDescription } from "@/app/components/codearena/problem-description"
import { CodeEditor } from "@/app/components/codearena/code-editor"
import { submitCode } from "@/lib/submission_api"
import { pollSubmission } from "@/lib/fetch_submission_api"
import { generateProblem } from "@/lib/get_problem_api"
import { getCachedProblem, setCachedProblem, clearProblemCache } from "@/lib/problem-cache"
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels"
import { Loader2, ArrowLeft, GripHorizontal, Play, Moon, Sun, Copy, Check } from "lucide-react"
import languageMapping from '@/app/components/language_mapping.json'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/app/components/ui/select"
import { Timer } from "@/app/components/ui/timer"
import { Button } from "@/app/components/ui/button"
import { getCategoryDisplayName } from "@/lib/categories"

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

interface TestResults {
  submitted: boolean;
  completed: boolean;
  passed: boolean;
  results: TestCaseResult[];
}

const languages = Object.entries(languageMapping.languages).map(([key, lang]) => ({
  id: lang.codeInt.toString(),
  name: lang.displayName
}))

function LoadingOverlay({ message }: { message: string }) {
  return (
    <div className="absolute inset-0 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm z-50 flex items-center justify-center transition-all duration-300">
      <div className="text-center">
        <Loader2 className="h-12 w-12 animate-spin text-indigo-600 mx-auto" />
        <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">{message}</p>
      </div>
    </div>
  );
}

export default function CodeArena({ category, onBack }: CodeArenaProps) {
  const [code, setCode] = useState("")
  const [language, setLanguage] = useState("91") // Default to Java
  const [status, setStatus] = useState("")
  const [loading, setLoading] = useState(true)
  const [isGenerating, setIsGenerating] = useState(false)
  const [problem, setProblem] = useState<{
    title: string;
    difficulty: string;
    description: string;
    testCases: { input: string[]; output: string; }[];
    structure: {
      problem_name: string;
      function_name: string;
      input_structure: Array<{ Input_Field: string }>;
      output_structure: { Output_Field: string };
    };
    javaBoilerplate: string;
    pythonBoilerplate: string;
    tags?: string[];
    concept?: string;
  }>({
    title: "",
    difficulty: "Medium",
    description: "",
    testCases: [],
    structure: {
      problem_name: "",
      function_name: "",
      input_structure: [],
      output_structure: { Output_Field: "" }
    },
    javaBoilerplate: "",
    pythonBoilerplate: "",
    tags: [],
    concept: ""
  })
  const [testResults, setTestResults] = useState<TestResults>({
    submitted: false,
    completed: false,
    passed: false,
    results: []
  });
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [editorTheme, setEditorTheme] = useState("vs-dark")
  const [showCopied, setShowCopied] = useState(false)

  // Debug logs for state changes
  useEffect(() => {
    console.log('=== State Change Debug ===');
    console.log('isGenerating:', isGenerating);
    console.log('code:', code);
    console.log('loading:', loading);
  }, [isGenerating, code, loading]);

  // Add effect to handle language changes
  useEffect(() => {
    if (!problem) return;
    
    // Update code with appropriate boilerplate when language changes
    const boilerplate = language === "91" ? problem.javaBoilerplate : problem.pythonBoilerplate;
    setCode(boilerplate || "");
  }, [language]);

  const toggleTheme = () => {
    setEditorTheme(prev => prev === "vs-dark" ? "vs-light" : "vs-dark")
  }

  const generateNewProblem = async () => {
    if (!category) {
      setLoading(false);
      return;
    }
    
    console.log('=== Generate New Problem ===');
    console.log('Category:', category);
    
    // Map category to backend concept
    const concept = category;
    const complexity = "EASY";
    
    try {
      // Check cache first
      console.log('Checking cache for category:', category);
      const cachedProblem = getCachedProblem(category);

      if (cachedProblem) {
        console.log('Found cached problem:', {
          title: cachedProblem.problem_title,
          hasBoilerplate: !!cachedProblem.java_boilerplate
        });
        
        const newProblem = {
          title: cachedProblem.problem_title,
          difficulty: cachedProblem.difficulty,
          description: cachedProblem.problem_statement,
          testCases: cachedProblem.test_cases,
          structure: cachedProblem.structure,
          javaBoilerplate: cachedProblem.java_boilerplate,
          pythonBoilerplate: cachedProblem.python_boilerplate,
          tags: cachedProblem.tags,
          concept: cachedProblem.concept
        };
        
        setProblem(newProblem);
        // Set initial code based on selected language
        const boilerplate = language === "91" ? newProblem.javaBoilerplate : newProblem.pythonBoilerplate;
        setCode(boilerplate || "");
      } else {
        console.log('No cache found, fetching from API');
        setIsGenerating(true);
        const apiProblem = await generateProblem(concept, complexity);
        
        const newProblem = {
          title: apiProblem.problem_title,
          difficulty: apiProblem.difficulty,
          description: apiProblem.problem_statement,
          testCases: apiProblem.test_cases,
          structure: apiProblem.structure,
          javaBoilerplate: apiProblem.java_boilerplate,
          pythonBoilerplate: apiProblem.python_boilerplate,
          tags: apiProblem.tags,
          concept: apiProblem.concept
        };
        
        setProblem(newProblem);
        // Set initial code based on selected language
        const boilerplate = language === "91" ? newProblem.javaBoilerplate : newProblem.pythonBoilerplate;
        setCode(boilerplate || "");
        
        // Cache the new problem
        setCachedProblem(category, apiProblem);
      }
      
      setTestResults({
        submitted: false,
        completed: false,
        passed: false,
        results: []
      });
      setStatus("");
    } catch (error) {
      console.error("Failed to generate new problem:", error);
      setStatus("Failed to generate problem. Please try again.");
    } finally {
      setIsGenerating(false);
      setLoading(false);
    }
  };

  useEffect(() => {
    generateNewProblem();
  }, [category]);

  const handleGenerateNew = () => {
    if (category) {
      // Clear the cache for this category before generating new problem
      clearProblemCache(category);
      generateNewProblem();
    }
  }

  const handleSubmit = async () => {
    try {
      setIsSubmitting(true);
      setTestResults({
        submitted: true,
        completed: false,
        passed: false,
        results: []
      });

      // 1. Submit the code and get submission tokens
      const tokens = await submitCode(
        code,
        language,
        JSON.stringify(problem.structure),
        problem.testCases || []
      );

      // 2. Poll for results with concept and difficulty
      const result = await pollSubmission(tokens.map(t => t.token), category, problem.difficulty);

      // 3. Update the test results
      setTestResults({
        submitted: true,
        completed: true,
        passed: result.passed,
        results: result.results
      });

      // 4. Update status message
      setStatus(result.passed ? "All tests passed!" : "Some tests failed.");

    } catch (error) {
      console.error('Error in handleSubmit:', error);
      setStatus(error instanceof Error ? error.message : 'Submission failed');
      setTestResults({
        submitted: false,
        completed: false,
        passed: false,
        results: []
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCopyCode = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setShowCopied(true)
      setTimeout(() => setShowCopied(false), 2000) // Hide after 2 seconds
    } catch (err) {
      console.error('Failed to copy code:', err)
    }
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-[calc(100vh-73px)]">
        <Loader2 className="h-12 w-12 animate-spin text-indigo-600" />
        <p className="mt-4 text-lg text-gray-600">Loading your coding challenge...</p>
      </div>
    )
  }

  console.log('=== CodeArena Render ===');
  console.log('Problem structure:', problem?.structure);

  return (
    <div id="code-arena-container" className="relative flex flex-col h-[calc(100vh-73px)]">
      {/* Loading overlay */}
      {isGenerating && (
        <LoadingOverlay message="Loading new challenge..." />
      )}

      <div className="flex-none h-12 bg-white px-4">
        <div className="max-w-7xl mx-auto w-full h-full flex items-center justify-between">
          <button 
            onClick={onBack}
            className="flex items-center gap-1.5 text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-50 py-1.5 px-2 transition-colors text-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back</span>
          </button>

          <div className="absolute left-1/2 -translate-x-1/2 flex items-center gap-4">
            <Select value={language} onValueChange={setLanguage} disabled={isGenerating}>
              <SelectTrigger className="w-[180px] bg-white border-2">
                <SelectValue placeholder="Select language" />
              </SelectTrigger>
              <SelectContent className="bg-white border-2">
                {languages.map((lang) => (
                  <SelectItem 
                    key={lang.id} 
                    value={lang.id} 
                    className="hover:bg-gray-100 text-gray-900 cursor-pointer"
                  >
                    {lang.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Button 
              onClick={handleSubmit} 
              size="sm"
              variant="outline"
              className="gap-2 text-gray-700 hover:text-gray-900 hover:bg-gray-100/80 border-2 border-green-500"
              disabled={isGenerating || isSubmitting}
            >
              {isSubmitting ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Play className="w-4 h-4 text-green-500" fill="currentColor" />
              )}
              {isSubmitting ? 'Running...' : 'Run'}
            </Button>

            <Timer />
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={handleCopyCode}
              className="w-9 h-9 hover:bg-gray-100 relative group"
            >
              {showCopied ? (
                <>
                  <Check className="h-4 w-4 text-green-600" />
                  <span className="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                    Copied!
                  </span>
                </>
              ) : (
                <>
                  <Copy className="h-4 w-4 text-gray-600" />
                  <span className="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                    Copy code
                  </span>
                </>
              )}
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              className="w-9 h-9 hover:bg-gray-100 relative group"
            >
              {editorTheme === "vs-dark" ? (
                <>
                  <Sun className="h-4 w-4 text-gray-600" />
                  <span className="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                    Light mode
                  </span>
                </>
              ) : (
                <>
                  <Moon className="h-4 w-4 text-gray-600" />
                  <span className="absolute -top-8 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                    Dark mode
                  </span>
                </>
              )}
            </Button>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        <PanelGroup direction="horizontal" className="h-full">
          <Panel defaultSize={40} minSize={30}>
            <div className="h-full overflow-hidden border-r border-border">
              <ProblemDescription
                title={problem?.title}
                difficulty={problem?.difficulty}
                description={problem?.description}
                displayCategory={getCategoryDisplayName(category || '')}
                backendCategory={category}
                onGenerateNewProblem={handleGenerateNew}
                isGenerating={isGenerating}
                tags={problem?.tags}
                chatContext={{
                  userId: 'guest',
                  concept: problem?.concept,
                  complexity: problem?.difficulty,
                  keywords: problem?.tags,
                  problemTitle: problem?.title,
                  problemDescription: problem?.description,
                  programmingLanguage: languages.find(l => l.id === language)?.name || 'Java',
                  currentCode: code,
                  testCases: problem?.testCases,
                  submissionResults: testResults,
                }}
              />
            </div>
          </Panel>

          <PanelResizeHandle className="w-2 bg-border hover:bg-muted/50 cursor-col-resize flex items-center justify-center">
            <div className="w-4 h-full flex items-center justify-center hover:bg-muted/80">
              <GripHorizontal className="h-2.5 w-2.5 text-gray-400" />
            </div>
          </PanelResizeHandle>

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
                isGenerating={isGenerating}
                editorTheme={editorTheme}
              />
            </div>
          </Panel>
        </PanelGroup>
      </div>
    </div>
  )
}
