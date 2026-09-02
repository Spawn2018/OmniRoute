import { createFileRoute } from "@tanstack/react-router"
import { CashFlowPage } from "@/features/cash-flow/catalog-page"

export const Route = createFileRoute("/cashflows")({
  component: CashFlowPage,
})
