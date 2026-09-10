import { createFileRoute } from "@tanstack/react-router"
import { VisibilityConnectorDesk } from "@/features/visibility-connector/catalog-page"

export const Route = createFileRoute("/visibility-connectors")({
  component: VisibilityConnectorDesk,
})
