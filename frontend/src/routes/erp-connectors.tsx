import { createFileRoute } from "@tanstack/react-router"
import { ErpConnectorDesk } from "@/features/erp-connector/catalog-page"

export const Route = createFileRoute("/erp-connectors")({
  component: ErpConnectorDesk,
})
