import { createFileRoute } from "@tanstack/react-router"
import { IdpConnectorDesk } from "@/features/idp-connector/catalog-page"

export const Route = createFileRoute("/idp-connectors")({
  component: IdpConnectorDesk,
})
