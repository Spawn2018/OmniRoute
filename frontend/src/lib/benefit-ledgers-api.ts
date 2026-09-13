import { ApiError, httpErrorStatus, readApiDetail } from "@/lib/api"
import { requireAuthHeaders } from "@/lib/tenant"

export type BenefitLedgerRow = {
  id: string
  organization_id: string
  benefit_code: string
  method_label: string
  hours_saved: string
  saved_amount: string
  saved_currency: string
  source_ref: string
}

export type BenefitLedgerPayload = {
  benefit_code: string
  method_label: string
  hours_saved: string
  saved_amount: string
  saved_currency: string
  source_ref: string
}

const ENDPOINT = "/api/v1/benefit-ledgers" as const

function authJsonHeaders(extra?: Record<string, string>): HeadersInit {
  return {
    ...requireAuthHeaders(),
    Accept: "application/json",
    ...extra,
  }
}

export function makeBenefitLedgerPayload(draft: {
  benefitCode: string
  methodLabel: string
  hoursSaved: string
  savedAmount: string
  savedCurrency: string
  sourceRef: string
}): BenefitLedgerPayload {
  return {
    benefit_code: draft.benefitCode.trim(),
    method_label: draft.methodLabel.trim(),
    hours_saved: draft.hoursSaved.trim(),
    saved_amount: draft.savedAmount.trim(),
    saved_currency: draft.savedCurrency.trim(),
    source_ref: draft.sourceRef.trim(),
  }
}

export async function loadBenefitLedgers(): Promise<BenefitLedgerRow[]> {
  const response = await fetch(ENDPOINT, { headers: authJsonHeaders() })
  if (!response.ok) {
    throw new ApiError(
      await readApiDetail(response, "Katalog ledgeru oszczędności niedostepny"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as BenefitLedgerRow[]
}

export async function createBenefitLedger(
  payload: BenefitLedgerPayload,
): Promise<BenefitLedgerRow> {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: authJsonHeaders({
      "Content-Type": "application/json",
      "X-Omni-Intent": "benefit-ledger-hitl",
    }),
    body: JSON.stringify(payload),
  })
  if (response.status !== 201) {
    throw new ApiError(
      await readApiDetail(response, "Zapis ledgeru oszczędności odrzucony"),
      httpErrorStatus(response),
    )
  }
  return (await response.json()) as BenefitLedgerRow
}
