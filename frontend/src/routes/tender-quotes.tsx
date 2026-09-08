import { createFileRoute } from "@tanstack/react-router"
import { BidDesk } from "@/features/tender-quote/catalog-page"

export const Route = createFileRoute("/tender-quotes")({
  component: BidDesk,
})
