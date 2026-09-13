import { createFileRoute } from "@tanstack/react-router"
import { BenefitLedgerBoard } from "@/features/benefit-ledger/catalog-page"

export const Route = createFileRoute("/benefit-ledgers")({
  component: BenefitLedgerBoard,
})
