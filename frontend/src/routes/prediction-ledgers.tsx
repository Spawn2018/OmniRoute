import { createFileRoute } from "@tanstack/react-router"
import { LedgerDesk } from "@/features/prediction-ledgers/catalog-page"

export const Route = createFileRoute("/prediction-ledgers")({
  component: LedgerDesk,
})
