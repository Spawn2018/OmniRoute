import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type BankPaymentRow = {
  id: string
  organization_id: string
  sales_invoice_id: string
  party_bank_account_id: string
  source_ref: string
}

const PAYMENTS_URL = "/api/v1/bank-payments"

async function parsePayment(response: Response, fallback: string): Promise<BankPaymentRow> {
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, fallback), httpErrorStatus(response))
  }
  return (await response.json()) as BankPaymentRow
}

export async function fetchBankPayments(): Promise<BankPaymentRow[]> {
  const response = await fetch(PAYMENTS_URL, { headers: requireAuthHeaders() })
  if (!response.ok) {
    throw new ApiError(await readApiDetail(response, "Błąd listy płatności"), httpErrorStatus(response))
  }
  return (await response.json()) as BankPaymentRow[]
}

export async function recordBankPayment(input: {
  sales_invoice_id: string
  party_bank_account_id: string
  source_ref: string
}): Promise<BankPaymentRow> {
  return parsePayment(
    await fetch(PAYMENTS_URL, {
      method: "POST",
      headers: { ...requireAuthHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify(input),
    }),
    "Błąd zapisu płatności",
  )
}
