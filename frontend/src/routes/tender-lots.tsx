import { createFileRoute } from "@tanstack/react-router"
import { LotDesk } from "@/features/tender-lot/catalog-page"

export const Route = createFileRoute("/tender-lots")({
  component: LotDesk,
})
