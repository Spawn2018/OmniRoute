import { createFileRoute } from "@tanstack/react-router"
import { ObservabilityPage } from "@/features/observability/catalog-page"

export const Route = createFileRoute("/health")({
  component: ObservabilityPage,
})
