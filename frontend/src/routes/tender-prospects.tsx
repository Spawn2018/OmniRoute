import { createFileRoute } from "@tanstack/react-router"
import { ProspectDesk } from "@/features/tender-prospect/catalog-page"

export const Route = createFileRoute("/tender-prospects")({
  component: ProspectDesk,
})
