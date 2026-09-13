import { createFileRoute } from "@tanstack/react-router"
import { VersionScoreBoard } from "@/features/version-score/catalog-page"

export const Route = createFileRoute("/version-scores")({
  component: VersionScoreBoard,
})
