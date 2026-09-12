import { createFileRoute } from "@tanstack/react-router"
import { SpotContractMarkBoard } from "@/features/spot-contract-mark/catalog-page"

export const Route = createFileRoute("/spot-contract-marks")({
  component: SpotContractMarkBoard,
})
