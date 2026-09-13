import { createFileRoute } from "@tanstack/react-router"
import { CounterfactualRunBoard } from "@/features/counterfactual-run/catalog-page"

export const Route = createFileRoute("/counterfactual-runs")({
  component: CounterfactualRunBoard,
})
