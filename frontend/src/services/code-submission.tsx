import { submitCode as submitCodeAPI } from "@/lib/submission_api"
import { pollSubmission } from "@/lib/fetch_submission_api"
import type { SubmissionStatus } from "@/lib/fetch_submission_api"

interface TestCase {
  input: any[]
  output: any
}

export async function submitCode(
  code: string, 
  language: string,
  structure: string,
  test_cases: TestCase[]
): Promise<{ status: { description: string; results: any[] } }> {
  console.log('=== Code Submission Service ===');
  
  const submission = await submitCodeAPI(code, language, structure, test_cases);
  console.log('Submission response:', submission);
  
  if (!Array.isArray(submission) || submission.length === 0) {
    throw new Error('Invalid response from Judge0');
  }

  const tokens = submission.map(s => s.token);
  console.log('Polling with tokens:', tokens);
  
  const status = await pollSubmission(tokens);
  console.log('Final status:', status);
  
  return { 
    status: {
      description: status.passed ? 'All tests passed' : 'Some tests failed',
      results: status.results
    } 
  };
}

