import { quotationAcceptancePending, type Quotation } from "@/lib/quotations-api"

export type OperatorNotice = {
  kind: "extraction_draft" | "offer_acceptance"
  id: string
  href: "/extractions" | "/quotations"
  label: string
  amount: string | null
  currency: string | null
}

export function operatorNotices(
  drafts: readonly { id: string; status: string; source_ref: string }[],
  quotations: readonly Quotation[],
): OperatorNotice[] {
  const notices: OperatorNotice[] = []
  for (const draft of drafts) {
    if (draft.status !== "pending") {
      continue
    }
    notices.push({
      kind: "extraction_draft",
      id: draft.id,
      href: "/extractions",
      label: draft.source_ref,
      amount: null,
      currency: null,
    })
  }
  for (const row of quotationAcceptancePending(quotations)) {
    notices.push({
      kind: "offer_acceptance",
      id: row.id,
      href: "/quotations",
      label: row.charge_code,
      amount: row.amount,
      currency: row.currency,
    })
  }
  return notices
}
