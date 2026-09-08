import { createFileRoute } from "@tanstack/react-router"
import { LaneDesk } from "@/features/tender-lane/catalog-page"

export const Route = createFileRoute("/tender-lanes")({
  component: LaneDesk,
})
