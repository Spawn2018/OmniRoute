import { createFileRoute } from "@tanstack/react-router"
import { OceanFeederMarkBoard } from "@/features/ocean-feeder-mark/catalog-page"

export const Route = createFileRoute("/ocean-feeder-marks")({
  component: OceanFeederMarkBoard,
})
