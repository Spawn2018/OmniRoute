import { createFileRoute } from "@tanstack/react-router"
import { HighValueMarkBoard } from "@/features/high-value-mark/catalog-page"

export const Route = createFileRoute("/high-value-marks")({
  component: HighValueMarkBoard,
})
