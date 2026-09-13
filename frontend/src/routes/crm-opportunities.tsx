import { createFileRoute } from "@tanstack/react-router"
import { CrmOpportunityDesk } from "@/features/crm-opportunity/catalog-page"

export const Route = createFileRoute("/crm-opportunities")({
  component: CrmOpportunityDesk,
})
