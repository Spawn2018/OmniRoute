import { createFileRoute } from "@tanstack/react-router"
import { AbandonedRtoBoard } from "@/features/abandoned-rto-mark/catalog-page"

export const Route = createFileRoute("/abandoned-rto-marks")({
  component: AbandonedRtoBoard,
})
