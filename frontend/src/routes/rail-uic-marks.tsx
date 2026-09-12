import { createFileRoute } from "@tanstack/react-router"
import { RailUicMarkBoard } from "@/features/rail-uic-mark/catalog-page"

export const Route = createFileRoute("/rail-uic-marks")({
  component: RailUicMarkBoard,
})
