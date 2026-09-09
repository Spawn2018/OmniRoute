import { createFileRoute } from "@tanstack/react-router"
import { IntakeDesk } from "@/features/tender-rfp-intake/catalog-page"

export const Route = createFileRoute("/tender-rfp-intakes")({
  component: IntakeDesk,
})
