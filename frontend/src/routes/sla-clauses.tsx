import { createFileRoute } from "@tanstack/react-router"
import { SlaClauseDesk } from "@/features/sla-clause/catalog-page"

export const Route = createFileRoute("/sla-clauses")({
  component: SlaClauseDesk,
})
