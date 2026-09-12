import { createFileRoute } from "@tanstack/react-router"
import { PalletPoolDesk } from "@/features/pallet-pool-mark/catalog-page"

export const Route = createFileRoute("/pallet-pool-marks")({
  component: PalletPoolDesk,
})
