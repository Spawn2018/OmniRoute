import { createFileRoute } from "@tanstack/react-router"
import { PalletSynchroMarkDesk } from "@/features/pallet-synchro-mark/catalog-page"

export const Route = createFileRoute("/pallet-synchro-marks")({
  component: PalletSynchroMarkDesk,
})
