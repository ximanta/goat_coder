interface ProblemResponse {
  concept: string;
  difficulty: "Easy" | "Medium" | "Hard";
  problem_title: string;
  problem_statement: string;
  /* eslint-disable @typescript-eslint/no-explicit-any */

  test_cases: {
    input: any[];
    output: any;
  }[];
  /* eslint-enable @typescript-eslint/no-explicit-any */

  tags: string[];
  structure: {
    problem_name: string;
    function_name: string;
    input_structure: Array<{ Input_Field: string }>;
    output_structure: { Output_Field: string };
  };
  java_boilerplate: string;
  python_boilerplate: string;
}

export type { ProblemResponse };
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function generateProblem(concept: string, complexity: string): Promise<ProblemResponse> {
  console.log('=== generateProblem API Call ===');
  console.log('Sending to backend:', { concept, complexity });

  try {
    const response = await fetch(`${API_BASE_URL}/problem-generator/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        concept,
        complexity,
      }),
    });

    console.log('Response status:', response.status);
    console.log('Response headers:', Object.fromEntries(response.headers.entries()));

    const responseText = await response.text();
    console.log('Raw response text:', responseText);

    if (!response.ok) {
      console.error('API Error:', responseText);
      throw new Error(`Failed to generate problem: ${responseText}`);
    }

    try {
      const data = JSON.parse(responseText);
      console.log('Parsed response data:', {
        concept: data.concept,
        difficulty: data.difficulty,
        problem_title: data.problem_title,
        test_cases: data.test_cases,
        structure: data.structure
      });
      
      // Log specific test case values
      if (data.test_cases) {
        console.log('Test cases detail:');
        data.test_cases.forEach((testCase: any, index: number) => {
          console.log(`Test case ${index + 1}:`, {
            input: testCase.input,
            inputTypes: testCase.input.map((val: any) => typeof val),
            output: testCase.output,
            outputType: typeof testCase.output
          });
        });
      }

      return data;
    } catch (parseError) {
      console.error('JSON Parse Error:', parseError);
      console.error('Failed to parse response:', responseText);
      throw new Error(`Failed to parse response: ${parseError}`);
    }
  } catch (error) {
    console.error('Network or processing error:', error);
    throw error;
  }
} 