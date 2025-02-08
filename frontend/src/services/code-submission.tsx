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
): Promise<{ status: SubmissionStatus }> {
  console.log('=== Code Submission Service ===');
  console.log('Submitting:', {
    codeLength: code.length,
    language,
    structure,
    testCasesCount: test_cases.length
  });
  
  const submission = await submitCodeAPI(code, language, structure, test_cases);
  console.log('Submission response:', submission);
  
  // Judge0 batch submission returns an array of submissions
  if (!Array.isArray(submission) || submission.length === 0) {
    console.error('Invalid submission response:', submission);
    throw new Error('Invalid response from Judge0');
  }

  const token = submission[0].token;
  if (!token) {
    console.error('No token in submission:', submission[0]);
    throw new Error('No submission token received from Judge0');
  }

  console.log('Polling with token:', token);
  const status = await pollSubmission(token);
  console.log('Final status:', status);
  
  return { status };
}

