import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type BookkeepingRow = {
  id: string
  organization_id: string
  charge_id: string
  sales_invoice_id: string
  source_ref: string
}

const BOOKKEEPING_URL = "/api/v1/bookkeepings"

export async function fetchBookkeeping(): Promise<BookkeepingRow[]> {
  const response = await fetch(BOOKKEEPING_URL, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy dekretów"), httpErrorStatus(response))
  }
  return (await response.json()) as BookkeepingRow[]
}

export async function recordBookkeeping(input: {
  charge_id: string
  sales_invoice_id: string
  source_ref: string
}): Promise<BookkeepingRow> {
  const response = await fetch(BOOKKEEPING_URL, {
    method: "POST",
    headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd zapisu dekretu"), httpErrorStatus(response))
  }
  return (await response.json()) as BookkeepingRow
}
