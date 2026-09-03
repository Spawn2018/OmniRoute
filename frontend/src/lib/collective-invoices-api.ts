import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type CollectiveInvoiceRow = {
  id: string
  organization_id: string
  sales_invoice_id: string
  shipment_id: string
  source_ref: string
}

const COLLECTIVE_URL = "/api/v1/collective-invoices"

export async function fetchCollectiveInvoices(): Promise<CollectiveInvoiceRow[]> {
  const response = await fetch(COLLECTIVE_URL, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy zbiorczych"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CollectiveInvoiceRow[]
}

export async function recordCollectiveInvoice(input: {
  sales_invoice_id: string
  shipment_id: string
  source_ref: string
}): Promise<CollectiveInvoiceRow> {
  const response = await fetch(COLLECTIVE_URL, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu zbiorczej"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as CollectiveInvoiceRow
}
