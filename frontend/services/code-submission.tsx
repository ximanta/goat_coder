import { submitCode as submitCodeAPI } from "@/lib/submission_api"
import { pollSubmission } from "@/lib/fetch_submission_api"
import type { SubmissionStatus } from "@/lib/fetch_submission_api"

export async function submitCode(code: string, language: string): Promise<{ status: SubmissionStatus }> {
  const submission = await submitCodeAPI(code, language)
  const status = await pollSubmission(submission.token)
  return { status }
}

