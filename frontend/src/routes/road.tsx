import { createFileRoute } from "@tanstack/react-router"
import { RoadTransportPage } from "@/features/road-transport/catalog-page"

export const Route = createFileRoute("/road")({
  component: RoadTransportPage,
})
