import { createFileRoute } from "@tanstack/react-router"
import { L3GateMarkDesk } from "@/features/l3-gate-mark/catalog-page"

export const Route = createFileRoute("/l3-gate-marks")({
  component: L3GateMarkDesk,
})
