import { createFileRoute } from "@tanstack/react-router"
import { PalletLedgerBoard } from "@/features/pallet-ledger/catalog-page"

export const Route = createFileRoute("/pallet-ledgers")({
  component: PalletLedgerBoard,
})
