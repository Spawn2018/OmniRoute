import { createFileRoute } from "@tanstack/react-router"
import { FreightTermMarkBoard } from "@/features/freight-term-mark/catalog-page"

export const Route = createFileRoute("/freight-term-marks")({
  component: FreightTermMarkBoard,
})
