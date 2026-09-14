import { createFileRoute } from "@tanstack/react-router"
import { LineImpactLayerMarkDesk } from "@/features/line-impact-layer-mark/catalog-page"

export const Route = createFileRoute("/line-impact-layer-marks")({
  component: LineImpactLayerMarkDesk,
})
