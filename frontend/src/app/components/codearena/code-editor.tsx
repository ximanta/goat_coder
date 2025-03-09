"use client"

import { useEffect, useRef, useState } from "react"
import { Editor } from "@monaco-editor/react"
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels"
import { TestCases } from "@/app/components/codearena/test-cases"
import languageMapping from '@/app/components/language_mapping.json'
import { GripVertical } from "lucide-react"

interface CodeEditorProps {
  code: string
  language: string
  onCodeChange: (code: string) => void
  structure: {
    problem_name: string;
    function_name: string;
    input_structure: Array<{ Input_Field: string }>;
    output_structure: { Output_Field: string };
  }
  testCases?: {
    input: any[];
    output: any;
  }[]
  javaBoilerplate?: string
  pythonBoilerplate?: string
  testResults?: {
    completed: boolean;
    passed: boolean;
    results: {
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
    }[];
  }
  isGenerating?: boolean
  editorTheme?: string
}

interface TestCaseResult {
  passed: boolean;
  stdout?: string;
  stderr?: string;
  compile_output?: string;
  expected_output?: string;
}

// Replace the hardcoded languages array with a transformed version from language_mapping
const languages = Object.entries(languageMapping.languages).map(([key, lang]) => ({
  id: lang.codeInt.toString(),  // Convert to string since Select expects string values
  name: lang.displayName
}))

export function CodeEditor({ 
  code, 
  language,
  onCodeChange,
  structure,
  testCases = [],
  javaBoilerplate = '',
  pythonBoilerplate = '',
  testResults,
  isGenerating = false,
  editorTheme = 'vs-dark'
}: CodeEditorProps) {
  const editorRef = useRef<any>(null)
  const initialLoadRef = useRef(true)

  // Debug logs for props changes
  useEffect(() => {
    console.log('=== CodeEditor Props Debug ===', {
      hasCode: !!code,
      language,
      isGenerating,
      hasStructure: !!structure,
      hasTestCases: testCases.length > 0,
      hasJavaBoilerplate: !!javaBoilerplate,
      hasPythonBoilerplate: !!pythonBoilerplate,
      isInitialLoad: initialLoadRef.current
    });
  }, [code, language, isGenerating, structure, testCases, javaBoilerplate, pythonBoilerplate]);

  // Only set boilerplate on initial load or language change
  useEffect(() => {
    if (!initialLoadRef.current) {
      console.log('Skipping boilerplate set - not initial load');
      return;
    }
    
    console.log('Setting initial boilerplate');
    const boilerplate = language === "91" ? javaBoilerplate : pythonBoilerplate;
    if (boilerplate && !code) {
      onCodeChange(boilerplate);
    }
    initialLoadRef.current = false;
  }, [language, javaBoilerplate, pythonBoilerplate]);

  const handleEditorChange = (value: string | undefined) => {
    console.log('=== Editor Change Debug ===', {
      newValue: !!value,
      isGenerating,
      willUpdate: !isGenerating
    });
    onCodeChange(value || "");
  };

  const handleEditorDidMount = (editor: any) => {
    editorRef.current = editor;
    console.log('=== Editor Mount Debug ===', {
      isReadOnly: editor.getOption(monaco.editor.EditorOption.readOnly),
      isDomReadOnly: editor.getOption(monaco.editor.EditorOption.domReadOnly),
      isGenerating
    });
  }

  useEffect(() => {
    return () => {
      if (editorRef.current) {
        editorRef.current.dispose()
      }
    }
  }, [])

  // Helper function to get Monaco editor language identifier
  const getMonacoLanguage = (codeInt: string) => {
    const languageEntry = Object.values(languageMapping.languages).find(
      lang => lang.codeInt.toString() === codeInt
    )
    if (!languageEntry) return 'plaintext'
    
    // Map the language to Monaco editor language identifier
    switch (languageEntry.displayName.toLowerCase()) {
      case 'python':
        return 'python'
      case 'java':
        return 'java'
      case 'c++':
        return 'cpp'
      case 'c':
        return 'c'
      case 'c#':
        return 'csharp'
      default:
        return 'plaintext'
    }
  }

  const handleSubmit = async () => {
    try {
      console.log('=== CodeEditor Submit ===');
      console.log('1. Initial structure prop:', structure);
      console.log('1a. Structure type:', typeof structure);
      
      if (!structure) {
        console.error('Structure is missing!');
        throw new Error('Problem structure is required');
      }

      if (!structure.function_name || !structure.input_structure || !structure.output_structure) {
        console.error('Structure is incomplete:', structure);
        throw new Error('Problem structure is incomplete');
      }

      // Use the structure directly from the problem generator
      const formattedStructure = {
        function_name: structure.function_name,
        input_structure: structure.input_structure,
        output_structure: structure.output_structure
      };
      
      const structureStr = JSON.stringify(formattedStructure);
      
      console.log('2. Formatted structure:', formattedStructure);
      console.log('3. Structure string:', structureStr);
      console.log('4. Test cases:', testCases);
      
      // Call submitCode with all required parameters
      const result = await submitCode(
        code,
        language,
        structureStr,
        testCases || []
      );
      
      console.log('5. Submit result:', result);
    } catch (error) {
      console.error('Error in handleSubmit:', error);
      // Show error to user
      alert(error instanceof Error ? error.message : 'An error occurred');
    }
  }

  const TestCaseResults: React.FC<{ results: TestCaseResult[] }> = ({ results }) => {
    return (
      <div className="space-y-4">
        {results.map((result, index) => (
          <div key={index} className={`p-4 rounded-lg ${result.passed ? 'bg-green-50' : 'bg-red-50'}`}>
            <div className="flex items-center gap-2">
              <span className={`text-sm font-medium ${result.passed ? 'text-green-600' : 'text-red-600'}`}>
                Test Case {index + 1}: {result.passed ? 'Passed' : 'Failed'}
              </span>
            </div>
            {!result.passed && (
              <div className="mt-2 text-sm">
                {result.compile_output && (
                  <div className="text-red-600">
                    <strong>Compilation Error:</strong>
                    <pre className="mt-1 text-xs">{result.compile_output}</pre>
                  </div>
                )}
                {result.stderr && (
                  <div className="text-red-600">
                    <strong>Runtime Error:</strong>
                    <pre className="mt-1 text-xs">{result.stderr}</pre>
                  </div>
                )}
                <div className="mt-2">
                  <strong>Expected:</strong> {result.expected_output}
                  <br />
                  <strong>Got:</strong> {result.stdout || 'No output'}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <PanelGroup direction="vertical" className="h-full">
      <Panel defaultSize={70} minSize={30}>
        <div className="flex flex-col h-full">
          <div className="flex-1 relative min-h-0 overflow-hidden">
            <Editor
              height="100%"
              language={getMonacoLanguage(language)}
              value={code}
              onChange={handleEditorChange}
              theme={editorTheme}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: "on",
                automaticLayout: true,
                scrollBeyondLastLine: false,
                wordWrap: "on",
                renderWhitespace: "selection",
                readOnly: false,
                domReadOnly: false,
              }}
              onMount={handleEditorDidMount}
              className="absolute inset-0"
            />
          </div>
        </div>
      </Panel>

      <PanelResizeHandle className="h-2 bg-border hover:bg-muted/50 cursor-row-resize flex items-center justify-center">
        <div className="h-4 w-full flex items-center justify-center hover:bg-muted/80">
          <GripVertical className="h-2.5 w-2.5 text-gray-400" />
        </div>
      </PanelResizeHandle>

      <Panel defaultSize={30} minSize={20}>
        <div className="h-full overflow-y-auto">
          <TestCases 
            testCases={testCases}
            results={testResults}
            structure={structure}
            isGenerating={isGenerating}
          />
        </div>
      </Panel>
    </PanelGroup>
  )
}
