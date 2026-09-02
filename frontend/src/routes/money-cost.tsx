import { createFileRoute } from "@tanstack/react-router"
import { MoneyCostPage } from "@/features/money-cost/catalog-page"

export const Route = createFileRoute("/money-cost")({
  component: MoneyCostPage,
})
