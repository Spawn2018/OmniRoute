import { createFileRoute } from "@tanstack/react-router"
import { PoPlantMarkBoard } from "@/features/po-plant-mark/catalog-page"

export const Route = createFileRoute("/po-plant-marks")({
  component: PoPlantMarkBoard,
})
