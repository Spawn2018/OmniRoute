import { createFileRoute } from "@tanstack/react-router"
import { PartnerExchangeBoard } from "@/features/partner-exchange-mark/catalog-page"

export const Route = createFileRoute("/partner-exchange-marks")({
  component: PartnerExchangeBoard,
})
