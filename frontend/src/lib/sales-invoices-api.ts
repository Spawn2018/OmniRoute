import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type SalesInvoice = {
  id: string
  organization_id: string
  shipment_id: string
  invoice_kind: string
  invoice_ref: string
  source_ref: string
  ksef_ref: string | null
  ksef_noted_at: string | null
}

export async function fetchSalesInvoices(): Promise<SalesInvoice[]> {
  const response = await fetch("/api/v1/sales-invoices", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy faktur"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as SalesInvoice[]
}

export async function createSalesInvoice(input: {
  shipment_id: string
  invoice_kind: string
  invoice_ref: string
  source_ref: string
}): Promise<SalesInvoice> {
  const response = await fetch("/api/v1/sales-invoices", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu faktury"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as SalesInvoice
}

export async function noteKsef(invoiceId: string, ksefRef: string): Promise<SalesInvoice> {
  const response = await fetch(`/api/v1/sales-invoices/${invoiceId}/note-ksef`, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify({ ksef_ref: ksefRef }),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu numeru sesji"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as SalesInvoice
}
