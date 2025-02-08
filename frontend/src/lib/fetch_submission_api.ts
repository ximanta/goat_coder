export interface SubmissionStatus {
  description: string;
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

interface TestCaseResult {
  test_case_index: number;
  token: string;
  status: {
    id: number;
    description: string;
  };
  compile_output?: string;
  stdout?: string;
  stderr?: string;
  expected_output?: string;
  passed: boolean;
  error?: string;
}

interface BatchSubmissionStatus {
  completed: boolean;
  passed: boolean;
  results: TestCaseResult[];
}

export async function pollSubmission(tokens: string[]): Promise<BatchSubmissionStatus> {
  if (!tokens.length) {
    throw new Error('No submission tokens provided');
  }

  const PROCESSING_STATUSES = [1, 2];

  while (true) {
    console.log('Polling submissions...');
    
    const response = await fetch(`http://localhost:8000/problem-submission/submissions-status`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tokens })
    });
    
    if (!response.ok) {
      throw new Error(`Failed to poll submissions: ${await response.text()}`);
    }

    const result = await response.json() as BatchSubmissionStatus;
    console.log('Poll result:', result);
    
    if (result.completed) {
      return result;
    }

    // Wait before polling again
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

