import { createFileRoute } from "@tanstack/react-router"
import { ImpactEdgeMarkDesk } from "@/features/impact-edge-mark/catalog-page"

export const Route = createFileRoute("/impact-edge-marks")({
  component: ImpactEdgeMarkDesk,
})
