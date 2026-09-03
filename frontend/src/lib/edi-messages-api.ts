import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type EdiMessage = {
  id: string
  organization_id: string
  shipment_id: string
  message_kind: string
  source_ref: string
}

export async function fetchEdiMessages(): Promise<EdiMessage[]> {
  const response = await fetch("/api/v1/edi-messages", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy komunikatów"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as EdiMessage[]
}

export async function createEdiMessage(input: {
  shipment_id: string
  message_kind: string
  source_ref: string
}): Promise<EdiMessage> {
  const response = await fetch("/api/v1/edi-messages", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu komunikatu"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as EdiMessage
}
