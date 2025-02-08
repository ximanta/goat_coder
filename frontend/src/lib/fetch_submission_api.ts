interface SubmissionStatus {
  status: {
    id: number
    description: string
  }
  compile_output?: string
  stdout?: string
  stderr?: string
  time?: number
  memory?: number
  exit_code?: number
  expected_output?: string
  // ... other fields as needed
}

export async function pollSubmission(token: string): Promise<SubmissionStatus> {
  if (!token) {
    console.error('Invalid token:', token);
    throw new Error('Cannot poll submission status: Invalid token');
  }

  // Define processing status IDs
  const PROCESSING_STATUSES = [1, 2]; // 1: In Queue, 2: Processing

  while (true) {
    console.log('Polling submission with token:', token);
    
    const response = await fetch(`http://localhost:8000/problem-submission/submission/${token}`);
    
    if (!response.ok) {
      const error = await response.text();
      console.error('Error polling submission:', error);
      throw new Error(`Failed to poll submission: ${error}`);
    }

    const result = await response.json();
    console.log('Poll result:', result);
    
    // If status is not "processing", return the result
    if (!PROCESSING_STATUSES.includes(result.status.id)) {
      return result;
    }

    // Wait 2 seconds before polling again
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

