interface ProblemResponse {
  concept: string;
  difficulty: string;
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
}

export async function generateProblem(concept: string = "array", complexity: string = "EASY"): Promise<ProblemResponse> {
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
    throw new Error("Failed to generate problem");
  }

  return response.json();
} 