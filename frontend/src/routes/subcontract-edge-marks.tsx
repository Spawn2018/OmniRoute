import { createFileRoute } from "@tanstack/react-router"
import { SubcontractEdgeMarkDesk } from "@/features/subcontract-edge-mark/catalog-page"

export const Route = createFileRoute("/subcontract-edge-marks")({
  component: SubcontractEdgeMarkDesk,
})
