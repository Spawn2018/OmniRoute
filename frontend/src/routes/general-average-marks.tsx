import { createFileRoute } from "@tanstack/react-router"
import { GeneralAverageBoard } from "@/features/general-average-mark/catalog-page"

export const Route = createFileRoute("/general-average-marks")({
  component: GeneralAverageBoard,
})
