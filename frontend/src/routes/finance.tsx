import { createFileRoute } from "@tanstack/react-router"
import { FinanceBoardPage } from "@/features/finance-board/catalog-page"

export const Route = createFileRoute("/finance")({
  component: FinanceBoardPage,
})
