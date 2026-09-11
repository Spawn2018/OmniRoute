import { createFileRoute } from "@tanstack/react-router"
import { CrmLeadDesk } from "@/features/crm-lead/catalog-page"

export const Route = createFileRoute("/crm-leads")({
  component: CrmLeadDesk,
})
