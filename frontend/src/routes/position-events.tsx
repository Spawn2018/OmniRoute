import { createFileRoute } from "@tanstack/react-router"
import { PositionEventDesk } from "@/features/position-event/catalog-page"

export const Route = createFileRoute("/position-events")({
  component: PositionEventDesk,
})
