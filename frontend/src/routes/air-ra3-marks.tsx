import { createFileRoute } from "@tanstack/react-router"
import { AirRa3MarkBoard } from "@/features/air-ra3-mark/catalog-page"

export const Route = createFileRoute("/air-ra3-marks")({
  component: AirRa3MarkBoard,
})
