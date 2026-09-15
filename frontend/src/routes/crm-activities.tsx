import { createFileRoute } from "@tanstack/react-router"
import { CrmActivityDesk } from "@/features/crm-activity/catalog-page"

export const Route = createFileRoute("/crm-activities")({
  component: CrmActivityDesk,
})
