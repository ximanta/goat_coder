interface TestCase {
  input: any[]
  output: any
}

interface ProblemStructure {
  function_name: string
  input_structure: Array<{ Input_Field: string }>
  output_structure: { Output_Field: string }
}

interface SubmissionRequest {
  language_id: string
  source_code: string
  problem_id: string
  structure: string  // JSON string of ProblemStructure
  test_cases: TestCase[]
}

interface SubmissionResponse {
  token: string;
}

export async function submitCode(
  code: string, 
  language: string, 
  structure: string,
  test_cases: TestCase[]
): Promise<SubmissionResponse[]> {
  console.log('=== Submission API ===');
  console.log('Request payload:', {
    language_id: language,
    source_code: code,
    problem_id: "123",
    structure,
    test_cases
  });

  const response = await fetch("http://localhost:8000/problem-submission/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      language_id: language,
      source_code: code,
      problem_id: "123",
      structure,
      test_cases
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error('Response error:', errorText);
    throw new Error(`Submission failed: ${errorText}`);
  }

  const result = await response.json();
  console.log('Submission result:', result);
  return result;
}

