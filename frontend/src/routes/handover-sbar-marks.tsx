import { createFileRoute } from "@tanstack/react-router"
import { HandoverSbarMarkDesk } from "@/features/handover-sbar-mark/catalog-page"

export const Route = createFileRoute("/handover-sbar-marks")({
  component: HandoverSbarMarkDesk,
})
