import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CreditReview = {
  id: string
  organization_id: string
  party_id: string
  review_date: string
  decision: string
  note: string | null
  source_ref: string
}

export function creditReviewCreateBody(input: {
  partyId: string
  reviewDate: string
  decision: string
  note: string
}): {
  party_id: string
  review_date: string
  decision: string
  note: string | null
} {
  const note = input.note.trim()
  return {
    party_id: input.partyId.trim(),
    review_date: input.reviewDate,
    decision: input.decision.trim().toLowerCase(),
    note: note === "" ? null : note,
  }
}

async function readCreditReview(response: Response, fallback: string): Promise<CreditReview> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as CreditReview
}

export async function fetchCreditReviews(): Promise<CreditReview[]> {
  const response = await fetch("/api/v1/credit-reviews", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy recenzji kredytowych"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CreditReview[]
}

export async function createCreditReview(body: {
  party_id: string
  review_date: string
  decision: string
  note: string | null
}): Promise<CreditReview> {
  const response = await fetch("/api/v1/credit-reviews", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readCreditReview(response, "Błąd zapisu recenzji kredytowej")
}

export async function resolveCreditReview(
  partyId: string,
  onDate: string,
): Promise<CreditReview> {
  const params = new URLSearchParams({ party_id: partyId, on_date: onDate })
  const response = await fetch(`/api/v1/credit-reviews/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readCreditReview(response, "Brak recenzji kredytowej")
}
