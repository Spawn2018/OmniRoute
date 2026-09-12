import { createFileRoute } from "@tanstack/react-router"
import { RailCimMarkBoard } from "@/features/rail-cim-mark/catalog-page"

export const Route = createFileRoute("/rail-cim-marks")({
  component: RailCimMarkBoard,
})
