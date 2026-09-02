import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CustomerSop = {
  id: string
  organization_id: string
  party_id: string
  code: string
  title: string
  body: string
  status: "draft" | "approved"
  approved_at: string | null
  source_ref: string
}

export type CustomerSopDraft = {
  partyId: string
  code: string
  title: string
  body: string
}

export const EMPTY_SOP_DRAFT: CustomerSopDraft = {
  partyId: "",
  code: "",
  title: "",
  body: "",
}

export function customerSopsForParty<
  Row extends { party_id: string },
>(sops: readonly Row[], partyId: string): Row[] {
  if (partyId === "") {
    return []
  }
  return sops.filter((row) => row.party_id === partyId)
}

export function customerSopCreateBody(draft: CustomerSopDraft): {
  party_id: string
  code: string
  title: string
  body: string
} {
  return {
    party_id: draft.partyId.trim(),
    code: draft.code.trim(),
    title: draft.title.trim(),
    body: draft.body.trim(),
  }
}

async function readSop(response: Response, fallback: string): Promise<CustomerSop> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as CustomerSop
}

export async function fetchCustomerSops(): Promise<CustomerSop[]> {
  const response = await fetch("/api/v1/customer-sops", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy procedur"), httpErrorStatus(response))
  }
  return (await response.json()) as CustomerSop[]
}

export async function createCustomerSop(
  body: ReturnType<typeof customerSopCreateBody>,
): Promise<CustomerSop> {
  const response = await fetch("/api/v1/customer-sops", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readSop(response, "Błąd zapisu procedury")
}

export async function resolveCustomerSop(partyId: string, code: string): Promise<CustomerSop> {
  const params = new URLSearchParams({ party_id: partyId, code })
  const response = await fetch(`/api/v1/customer-sops/resolve?${params.toString()}`, {
    headers: requireAuthHeaders(),
  })
  return readSop(response, "Nieznana procedura")
}

export async function approveCustomerSop(sopId: string): Promise<CustomerSop> {
  const response = await fetch(`/api/v1/customer-sops/${sopId}/approve`, {
    method: "POST",
    headers: requireAuthHeaders(),
  })
  return readSop(response, "Błąd zatwierdzenia procedury")
}
