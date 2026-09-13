import { createFileRoute } from "@tanstack/react-router"
import { SuggestionLedgerBoard } from "@/features/suggestion-ledger/catalog-page"

export const Route = createFileRoute("/suggestion-ledgers")({
  component: SuggestionLedgerBoard,
})
