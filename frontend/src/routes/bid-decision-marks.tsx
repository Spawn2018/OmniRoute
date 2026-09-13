import { createFileRoute } from "@tanstack/react-router"
import { BidDecisionMarkBoard } from "@/features/bid-decision-mark/catalog-page"

export const Route = createFileRoute("/bid-decision-marks")({
  component: BidDecisionMarkBoard,
})
