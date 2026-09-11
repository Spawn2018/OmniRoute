import { createFileRoute } from "@tanstack/react-router"
import { SapConnectorDesk } from "@/features/sap-connector/catalog-page"

export const Route = createFileRoute("/sap-connectors")({
  component: SapConnectorDesk,
})
