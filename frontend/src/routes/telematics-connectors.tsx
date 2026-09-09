import { createFileRoute } from "@tanstack/react-router"
import { ConnectorDesk } from "@/features/telematics-connector/catalog-page"

export const Route = createFileRoute("/telematics-connectors")({
  component: ConnectorDesk,
})
