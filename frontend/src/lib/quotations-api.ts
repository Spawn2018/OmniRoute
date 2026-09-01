import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type Quotation = {
  id: string
  organization_id: string
  charge_code: string
  rate_line_id: string
  amount: string
  currency: string
  source_ref: string
}

export function quotationCreateBody(chargeCode: string): { charge_code: string } {
  return { charge_code: chargeCode.trim() }
}

async function readQuotation(response: Response, fallback: string): Promise<Quotation> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as Quotation
}

export async function fetchQuotations(): Promise<Quotation[]> {
  const response = await fetch("/api/v1/quotations", { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy wycen"), httpErrorStatus(response))
  }
  return (await response.json()) as Quotation[]
}

export async function createQuotation(body: { charge_code: string }): Promise<Quotation> {
  const response = await fetch("/api/v1/quotations", {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return readQuotation(response, "Błąd wyceny")
}
