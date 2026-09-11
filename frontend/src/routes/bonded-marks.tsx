import { createFileRoute } from "@tanstack/react-router"
import { BondedMarkDesk } from "@/features/bonded-mark/catalog-page"

export const Route = createFileRoute("/bonded-marks")({
  component: BondedMarkDesk,
})
