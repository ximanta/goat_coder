interface ProblemResponse {
  concept: string;
  difficulty: "Easy" | "Medium" | "Hard";
  problem_title: string;
  problem_statement: string;
  test_cases: {
    input: any[];
    output: any;
  }[];
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

export async function generateProblem(concept: string, complexity: string): Promise<ProblemResponse> {
  console.log('=== generateProblem API Call ===');
  console.log('Sending to backend:', { concept, complexity });

  const response = await fetch("http://localhost:8000/problem-generator/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      concept,
      complexity,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error('API Error:', errorText);
    throw new Error(`Failed to generate problem: ${errorText}`);
  }

  const data = await response.json();
  console.log('Received from backend:', data);
  return data;
} 