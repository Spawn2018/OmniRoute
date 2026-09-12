import { createFileRoute } from "@tanstack/react-router"
import { DualLedgerMarkBoard } from "@/features/dual-ledger-mark/catalog-page"

export const Route = createFileRoute("/dual-ledger-marks")({
  component: DualLedgerMarkBoard,
})
