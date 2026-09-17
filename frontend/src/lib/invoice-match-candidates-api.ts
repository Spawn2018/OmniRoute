import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/invoice-match-candidates"

export type InvoiceMatchCandidateRow = {
  id: string
  organization_id: string
  candidate_code: string
  candidate_kind: string
  source_ref: string
}

export type InvoiceMatchCandidateWrite = {
  candidate_code: string
  candidate_kind: string
  source_ref: string
}

export function buildInvoiceMatchCandidateWrite(fields: {
  code: string
  kind: string
  origin: string
}): InvoiceMatchCandidateWrite {
  return {
    candidate_code: fields.code.trim(),
    candidate_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchInvoiceMatchCandidates(): Promise<InvoiceMatchCandidateRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Blad listy znacznikow kandydata dopasowania FV", 200)
}

export async function saveInvoiceMatchCandidate(
  body: InvoiceMatchCandidateWrite,
): Promise<InvoiceMatchCandidateRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Blad zapisu znacznika kandydata dopasowania FV", 201)
}
