import { createFileRoute } from "@tanstack/react-router"
import { ExchangeConnectorDesk } from "@/features/exchange-connector/catalog-page"

export const Route = createFileRoute("/exchange-connectors")({
  component: ExchangeConnectorDesk,
})
