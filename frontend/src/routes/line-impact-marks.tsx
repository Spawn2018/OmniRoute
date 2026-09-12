import { createFileRoute } from "@tanstack/react-router"
import { LineImpactMarkBoard } from "@/features/line-impact-mark/catalog-page"

export const Route = createFileRoute("/line-impact-marks")({
  component: LineImpactMarkBoard,
})
