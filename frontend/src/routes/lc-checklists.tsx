import { createFileRoute } from "@tanstack/react-router"
import { LcChecklistDesk } from "@/features/lc-checklist/catalog-page"

export const Route = createFileRoute("/lc-checklists")({
  component: LcChecklistDesk,
})
