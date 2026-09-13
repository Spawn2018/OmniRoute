import { createFileRoute } from "@tanstack/react-router"
import { FactoringConnectorDesk } from "@/features/factoring-connector/catalog-page"

export const Route = createFileRoute("/factoring-connectors")({
  component: FactoringConnectorDesk,
})
