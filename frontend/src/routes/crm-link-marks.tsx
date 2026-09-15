import { createFileRoute } from "@tanstack/react-router"
import { CrmLinkMarkDesk } from "@/features/crm-link-mark/catalog-page"

export const Route = createFileRoute("/crm-link-marks")({
  component: CrmLinkMarkDesk,
})
