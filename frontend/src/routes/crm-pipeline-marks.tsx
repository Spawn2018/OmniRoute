import { createFileRoute } from "@tanstack/react-router"
import { CrmPipelineMarkDesk } from "@/features/crm-pipeline-mark/catalog-page"

export const Route = createFileRoute("/crm-pipeline-marks")({
  component: CrmPipelineMarkDesk,
})
