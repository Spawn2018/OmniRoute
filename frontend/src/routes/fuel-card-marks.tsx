import { createFileRoute } from "@tanstack/react-router"
import { FuelCardMarkBoard } from "@/features/fuel-card-mark/catalog-page"

export const Route = createFileRoute("/fuel-card-marks")({
  component: FuelCardMarkBoard,
})
