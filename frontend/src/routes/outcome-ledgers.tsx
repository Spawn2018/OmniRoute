import { createFileRoute } from "@tanstack/react-router"
import { OutcomeLedgerBoard } from "@/features/outcome-ledger/catalog-page"

export const Route = createFileRoute("/outcome-ledgers")({
  component: OutcomeLedgerBoard,
})
