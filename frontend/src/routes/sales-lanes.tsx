import { createFileRoute } from "@tanstack/react-router"
import { SalesLaneDesk } from "@/features/sales-lane/catalog-page"

export const Route = createFileRoute("/sales-lanes")({
  component: SalesLaneDesk,
})
