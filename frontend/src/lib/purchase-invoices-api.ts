import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

const API = "/api/v1/purchase-invoices"

export type PurchaseInvoiceRow = {
  id: string
  organization_id: string
  invoice_ref: string
  invoice_kind: string
  source_ref: string
}

export type PurchaseInvoiceWrite = {
  invoice_ref: string
  invoice_kind: string
  source_ref: string
}

export function buildPurchaseInvoiceWrite(fields: {
  ref: string
  kind: string
  origin: string
}): PurchaseInvoiceWrite {
  return {
    invoice_ref: fields.ref.trim(),
    invoice_kind: fields.kind.trim().toLowerCase(),
    source_ref: fields.origin.trim(),
  }
}

async function asJson<T>(response: Response, whenFail: string, okStatus: number): Promise<T> {
  if (response.status !== okStatus) {
    throw new ApiError(await readApiDetail(response, whenFail), httpErrorStatus(response))
  }
  return (await response.json()) as T
}

export async function fetchPurchaseInvoices(): Promise<PurchaseInvoiceRow[]> {
  const response = await fetch(API, { headers: requireAuthHeaders() })
  return asJson(response, "Błąd listy faktur zakupu", 200)
}

export async function savePurchaseInvoice(
  body: PurchaseInvoiceWrite,
): Promise<PurchaseInvoiceRow> {
  const response = await fetch(API, {
    method: "POST",
    headers: {
      ...requireAuthHeaders(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
  return asJson(response, "Błąd zapisu faktury zakupu", 201)
}
