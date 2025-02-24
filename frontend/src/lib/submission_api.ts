/* eslint-disable @typescript-eslint/no-explicit-any */
interface TestCase {
  input: any[]
  output: any
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
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

  const response = await fetch(`${API_BASE_URL}/problem-submission/submit`, {
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

