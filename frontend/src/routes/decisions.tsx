import { createFileRoute } from "@tanstack/react-router"
import { OperatorDecisionCatalogPage } from "@/features/operator-decisions/catalog-page"

export const Route = createFileRoute("/decisions")({
  component: OperatorDecisionCatalogPage,
})
