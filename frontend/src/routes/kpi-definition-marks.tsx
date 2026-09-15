import { createFileRoute } from "@tanstack/react-router"
import { KpiDefinitionMarkDesk } from "@/features/kpi-definition-mark/catalog-page"

export const Route = createFileRoute("/kpi-definition-marks")({
  component: KpiDefinitionMarkDesk,
})
