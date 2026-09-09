import { createFileRoute } from "@tanstack/react-router"
import { StanceDesk } from "@/features/tender-bid-stance/catalog-page"

export const Route = createFileRoute("/tender-bid-stances")({
  component: StanceDesk,
})
