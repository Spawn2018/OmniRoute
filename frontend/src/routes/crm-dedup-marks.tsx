import { createFileRoute } from "@tanstack/react-router"
import { CrmDedupMarkDesk } from "@/features/crm-dedup-mark/catalog-page"

export const Route = createFileRoute("/crm-dedup-marks")({
  component: CrmDedupMarkDesk,
})
