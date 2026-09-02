import { createFileRoute } from "@tanstack/react-router"
import { TrackingPage } from "@/features/tracking/catalog-page"

export const Route = createFileRoute("/tracking")({
  component: TrackingPage,
})
