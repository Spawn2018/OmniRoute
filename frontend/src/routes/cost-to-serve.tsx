import { createFileRoute } from "@tanstack/react-router"
import { CostToServePage } from "@/features/cost-to-serve/catalog-page"

export const Route = createFileRoute("/cost-to-serve")({
  component: CostToServePage,
})
