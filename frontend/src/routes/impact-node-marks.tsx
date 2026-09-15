import { createFileRoute } from "@tanstack/react-router"
import { ImpactNodeMarkDesk } from "@/features/impact-node-mark/catalog-page"

export const Route = createFileRoute("/impact-node-marks")({
  component: ImpactNodeMarkDesk,
})
