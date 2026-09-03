import type { OperatorDecision } from "@/lib/operator-decisions-api"
import type { Quotation } from "@/lib/quotations-api"

export type QuotationOfferOutcome = {
  quotationId: string
  partyId: string
  status: "accepted" | "rejected"
  sourceRef: string
}

function quotationById(rows: Quotation[] | undefined): Map<string, Quotation> {
  const byId = new Map<string, Quotation>()
  for (const row of rows ?? []) {
    if (row.party_id === null) {
      continue
    }
    byId.set(row.id, row)
  }
  return byId
}

function isOfferVerdict(
  status: OperatorDecision["status"],
): status is "accepted" | "rejected" {
  return status === "accepted" || status === "rejected"
}

export function quotationOfferOutcomes(
  quotations: Quotation[] | undefined,
  decisions: OperatorDecision[] | undefined,
): QuotationOfferOutcome[] {
  const byId = quotationById(quotations)
  const rows: QuotationOfferOutcome[] = []
  for (const decision of decisions ?? []) {
    if (decision.subject_kind !== "quotation" || !isOfferVerdict(decision.status)) {
      continue
    }
    const quote = byId.get(decision.subject_id)
    if (quote === undefined || quote.party_id === null) {
      continue
    }
    rows.push({
      quotationId: quote.id,
      partyId: quote.party_id,
      status: decision.status,
      sourceRef: decision.source_ref,
    })
  }
  return rows
}
