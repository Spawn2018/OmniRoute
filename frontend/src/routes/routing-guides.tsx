import { createFileRoute } from "@tanstack/react-router"
import { RoutingGuideDesk } from "@/features/routing-guide/catalog-page"

export const Route = createFileRoute("/routing-guides")({
  component: RoutingGuideDesk,
})
