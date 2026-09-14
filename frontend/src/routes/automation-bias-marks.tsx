import { createFileRoute } from "@tanstack/react-router"
import { AutomationBiasMarkDesk } from "@/features/automation-bias-mark/catalog-page"

export const Route = createFileRoute("/automation-bias-marks")({
  component: AutomationBiasMarkDesk,
})
