import { createFileRoute } from "@tanstack/react-router"
import { RankDesk } from "@/features/rank-mark/catalog-page"

export const Route = createFileRoute("/rank-marks")({
  component: RankDesk,
})
