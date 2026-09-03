import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CarrierInquiry = {
  id: string
  organization_id: string
  network_member_id: string
  source_ref: string
  status: string
}

export async function fetchCarrierInquiries(): Promise<CarrierInquiry[]> {
  const response = await fetch("/api/v1/carrier-inquiries", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy zapytań do agentów"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CarrierInquiry[]
}

export async function createCarrierInquiry(networkMemberId: string): Promise<CarrierInquiry> {
  const response = await fetch("/api/v1/carrier-inquiries", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ network_member_id: networkMemberId }),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu zapytania do agenta"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CarrierInquiry
}
