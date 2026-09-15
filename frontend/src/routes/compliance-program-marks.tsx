import { createFileRoute } from "@tanstack/react-router"
import { ComplianceProgramMarkDesk } from "@/features/compliance-program-mark/catalog-page"

export const Route = createFileRoute("/compliance-program-marks")({
  component: ComplianceProgramMarkDesk,
})
