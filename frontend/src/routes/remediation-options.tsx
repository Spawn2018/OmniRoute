import { createFileRoute } from "@tanstack/react-router"
import { RemediationOptionDesk } from "@/features/remediation-option/catalog-page"

export const Route = createFileRoute("/remediation-options")({
  component: RemediationOptionDesk,
})
