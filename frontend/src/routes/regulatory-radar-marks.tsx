import { createFileRoute } from "@tanstack/react-router"
import { RegulatoryRadarBoard } from "@/features/regulatory-radar-mark/catalog-page"

export const Route = createFileRoute("/regulatory-radar-marks")({
  component: RegulatoryRadarBoard,
})
