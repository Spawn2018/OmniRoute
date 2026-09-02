import { createFileRoute } from "@tanstack/react-router"
import { OperatorNoticePage } from "@/features/operator-notice/catalog-page"

export const Route = createFileRoute("/notifications")({
  component: OperatorNoticePage,
})
