import { createFileRoute } from "@tanstack/react-router"
import { IntervalScoreBoard } from "@/features/interval-score/catalog-page"

export const Route = createFileRoute("/interval-scores")({
  component: IntervalScoreBoard,
})
