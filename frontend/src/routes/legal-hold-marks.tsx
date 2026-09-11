import { createFileRoute } from "@tanstack/react-router"
import { LegalHoldMarkDesk } from "@/features/legal-hold-mark/catalog-page"

export const Route = createFileRoute("/legal-hold-marks")({
  component: LegalHoldMarkDesk,
})
