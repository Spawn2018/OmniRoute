import { createFileRoute } from "@tanstack/react-router"
import { MatchKindBoard } from "@/features/routing-guide-match/catalog-page"

export const Route = createFileRoute("/routing-guide-matches")({
  component: MatchKindBoard,
})
