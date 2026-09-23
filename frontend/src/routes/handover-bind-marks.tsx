import { createFileRoute } from "@tanstack/react-router"
import { HandoverBindMarkDesk } from "@/features/handover-bind-mark/catalog-page"

export const Route = createFileRoute("/handover-bind-marks")({
  component: HandoverBindMarkDesk,
})
