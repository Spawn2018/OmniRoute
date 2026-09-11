import { createFileRoute } from "@tanstack/react-router"
import { FreightAuditMarkDesk } from "@/features/freight-audit-mark/catalog-page"

export const Route = createFileRoute("/freight-audit-marks")({
  component: FreightAuditMarkDesk,
})
