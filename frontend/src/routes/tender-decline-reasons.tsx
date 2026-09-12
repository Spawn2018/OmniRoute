import { createFileRoute } from "@tanstack/react-router"
import { TenderDeclineReasonBoard } from "@/features/tender-decline-reason/catalog-page"

export const Route = createFileRoute("/tender-decline-reasons")({
  component: TenderDeclineReasonBoard,
})
