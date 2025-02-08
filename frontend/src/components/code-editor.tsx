"use client"

import { useEffect, useRef } from "react"
import { Editor } from "@monaco-editor/react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels"
import { TestCases } from "./codearena/test-cases"
import languageMapping from './language_mapping.json'
import { submitCode } from "@/services/code-submission"

interface CodeEditorProps {
  code: string
  language: string
  onCodeChange: (code: string) => void
  onLanguageChange: (language: string) => void
  onSubmit: (result: { status: string }) => void
  status: string
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
  onLanguageChange, 
  onSubmit, 
  status, 
  structure, 
  testCases = [],
  javaBoilerplate = '',
  pythonBoilerplate = ''
}: CodeEditorProps) {
  const editorRef = useRef<any>(null)

  // Add useEffect to set initial boilerplate based on selected language
  useEffect(() => {
    if (language && !code) {  // Only set if language is selected and no code is present
      switch (language) {
        case '4': // Java
          onCodeChange(javaBoilerplate)
          break
        case '28': // Python
          onCodeChange(pythonBoilerplate)
          break
      }
    }
  }, [language, javaBoilerplate, pythonBoilerplate, code, onCodeChange])

  useEffect(() => {
    console.log('Language:', language)
    console.log('Java Boilerplate:', javaBoilerplate)
    console.log('Python Boilerplate:', pythonBoilerplate)
  }, [language, javaBoilerplate, pythonBoilerplate])

  useEffect(() => {
    console.log('CodeEditor State:', {
      language,
      code,
      javaBoilerplate,
      pythonBoilerplate,
      hasStructure: !!structure,
      hasTestCases: !!testCases?.length
    })
  }, [language, code, javaBoilerplate, pythonBoilerplate, structure, testCases])

  useEffect(() => {
    console.log('=== CodeEditor Mount ===');
    console.log('Initial props:', {
      structure,
      testCases: testCases?.length
    });
  }, []);

  const handleEditorDidMount = (editor: any) => {
    editorRef.current = editor
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

  // Add handler for language change that also updates the code
  const handleLanguageChange = (newLanguage: string) => {
    onLanguageChange(newLanguage)
    
    // Set appropriate boilerplate based on language
    switch (newLanguage) {
      case '4': // Java
        onCodeChange(javaBoilerplate)
        break
      case '28': // Python
        onCodeChange(pythonBoilerplate)
        break
      default:
        onCodeChange('')
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
      onSubmit(result);
    } catch (error) {
      console.error('Error in handleSubmit:', error);
      // Show error to user
      alert(error instanceof Error ? error.message : 'An error occurred');
    }
  }

  return (
    <PanelGroup direction="vertical" className="h-full">
      <Panel defaultSize={70} minSize={30}>
        <div className="flex flex-col h-full">
          <div className="flex items-center gap-4 p-4 border-b border-border bg-background">
            <Select value={language} onValueChange={handleLanguageChange}>
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
              size="lg" 
              className="bg-green-600 hover:bg-green-700 text-white px-8"
            >
              Submit
            </Button>
          </div>

          <div className="flex-1 relative min-h-0 overflow-hidden">
            <Editor
              height="100%"
              language={getMonacoLanguage(language)}
              value={code}
              onChange={(value) => onCodeChange(value || "")}
              theme="vs-dark"
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: "on",
                automaticLayout: true,
                scrollBeyondLastLine: false,
                wordWrap: "on",
                renderWhitespace: "selection",
              }}
              onMount={handleEditorDidMount}
              className="absolute inset-0"
            />
          </div>
        </div>
      </Panel>

      <PanelResizeHandle className="h-2 bg-border hover:bg-muted/50 cursor-row-resize" />

      <Panel defaultSize={30} minSize={20}>
        <div className="h-full overflow-y-auto">
          <TestCases testCases={testCases} results={{ status }} structure={structure} />
        </div>
      </Panel>
    </PanelGroup>
  )
}

