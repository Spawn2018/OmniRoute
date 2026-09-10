import { createFileRoute } from "@tanstack/react-router"
import { PlanningBoard } from "@/features/planning/catalog-page"

export const Route = createFileRoute("/planning")({
  component: PlanningBoard,
})
