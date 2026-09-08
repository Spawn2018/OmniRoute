import { createFileRoute } from "@tanstack/react-router"
import { PalletBalanceBoard } from "@/features/pallet-balance/catalog-page"

export const Route = createFileRoute("/pallet-balances")({
  component: PalletBalanceBoard,
})
