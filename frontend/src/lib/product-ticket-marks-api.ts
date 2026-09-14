import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type ProductTicketMarkRow = {
  id: string
  organization_id: string
  mark_code: string
  ticket_kind: string
  source_ref: string
}

export type ProductTicketMarkPayload = {
  mark_code: string
  ticket_kind: string
  source_ref: string
}

const ENDPOINT = "/api/v1/product-ticket-marks"

export function buildProductTicketMarkWrite(input: {
  code: string
  kind: string
  origin: string
}): ProductTicketMarkPayload {
  const mark_code = input.code.trim()
  const ticket_kind = input.kind.trim().toLowerCase()
  const source_ref = input.origin.trim()
  return { mark_code, ticket_kind, source_ref }
}

export async function fetchProductTicketMarks(): Promise<ProductTicketMarkRow[]> {
  const response = await fetch(ENDPOINT, {
    headers: { ...requireAuthHeaders(), Accept: "application/json" },
  })
  if (response.ok) {
    return (await response.json()) as ProductTicketMarkRow[]
  }
  throw new ApiError(
    await readApiDetail(response, "Nie udało się wczytać ticketów produktu"),
    httpErrorStatus(response),
  )
}

export async function saveProductTicketMark(
  body: ProductTicketMarkPayload,
): Promise<ProductTicketMarkRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-Omni-Intent": "product-ticket-hitl",
    },
    body: JSON.stringify(body),
  })
  if (response.status === 201) {
    return (await response.json()) as ProductTicketMarkRow
  }
  throw new ApiError(
    await readApiDetail(response, "Nie udało się zapisać ticketu produktu"),
    httpErrorStatus(response),
  )
}
