import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CustomerRfq = {
  id: string
  organization_id: string
  inbound_message_id: string
  source_ref: string
  status: string
  party_id: string | null
}

async function readCustomerRfq(response: Response, fallback: string): Promise<CustomerRfq> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as CustomerRfq
}

export async function fetchCustomerRfqs(): Promise<CustomerRfq[]> {
  const response = await fetch("/api/v1/customer-rfqs", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy zapytań ofertowych"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CustomerRfq[]
}

export async function createCustomerRfq(inboundMessageId: string): Promise<CustomerRfq> {
  const response = await fetch("/api/v1/customer-rfqs", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ inbound_message_id: inboundMessageId }),
  })
  return readCustomerRfq(response, "Błąd zapisu zapytania ofertowego")
}
