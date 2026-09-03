import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type QuoteInvoiceSettlement = {
  id: string
  organization_id: string
  quotation_id: string
  sales_invoice_id: string
  source_ref: string
}

export async function fetchQuoteInvoiceSettlements(): Promise<QuoteInvoiceSettlement[]> {
  const response = await fetch("/api/v1/quote-invoice-settlements", {
    headers: requireAuthHeaders(),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd listy rozliczeń"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as QuoteInvoiceSettlement[]
}

export async function createQuoteInvoiceSettlement(input: {
  quotation_id: string
  sales_invoice_id: string
  source_ref: string
}): Promise<QuoteInvoiceSettlement> {
  const response = await fetch("/api/v1/quote-invoice-settlements", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Błąd zapisu rozliczenia"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as QuoteInvoiceSettlement
}
