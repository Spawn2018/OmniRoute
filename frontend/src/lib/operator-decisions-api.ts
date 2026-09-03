import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type OperatorDecision = {
  id: string
  organization_id: string
  subject_kind: string
  subject_id: string
  status: "pending" | "accepted" | "changed" | "rejected"
  decided_at: string | null
  lock_version: number
  source_ref: string
}

export type OperatorDecisionDraft = {
  subjectId: string
  sourceRef: string
}

export const EMPTY_DECISION_DRAFT: OperatorDecisionDraft = {
  subjectId: "",
  sourceRef: "fixture://operator-decision/1",
}

export function operatorDecisionCreateBody(draft: OperatorDecisionDraft): {
  subject_kind: "inbound_message"
  subject_id: string
  source_ref: string
} {
  return {
    subject_kind: "inbound_message",
    subject_id: draft.subjectId.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

async function readDecision(response: Response, fallback: string): Promise<OperatorDecision> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as OperatorDecision
}

export async function fetchOperatorDecisions(): Promise<OperatorDecision[]> {
  const response = await fetch("/api/v1/operator-decisions", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy decyzji"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as OperatorDecision[]
}

export async function createOperatorDecision(body: {
  subject_kind: string
  subject_id: string
  source_ref: string
}): Promise<OperatorDecision> {
  const response = await fetch("/api/v1/operator-decisions", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readDecision(response, "Błąd zapisu decyzji")
}

export async function decideOperatorDecision(
  decisionId: string,
  status: "accepted" | "rejected",
  lockVersion: number,
): Promise<OperatorDecision> {
  const response = await fetch(`/api/v1/operator-decisions/${decisionId}/decide`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ status, lock_version: lockVersion }),
  })
  return readDecision(response, "Błąd zapisu werdyktu")
}
