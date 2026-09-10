import { createFileRoute } from "@tanstack/react-router"
import { ConsignmentBoard } from "@/features/consignment/catalog-page"

export const Route = createFileRoute("/consignments")({
  component: ConsignmentBoard,
})
