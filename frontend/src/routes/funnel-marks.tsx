import { createFileRoute } from "@tanstack/react-router"
import { FunnelMarkBoard } from "@/features/funnel-mark/catalog-page"

export const Route = createFileRoute("/funnel-marks")({
  component: FunnelMarkBoard,
})
