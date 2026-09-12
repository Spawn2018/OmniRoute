import { createFileRoute } from "@tanstack/react-router"
import { JobMetricMarkBoard } from "@/features/job-metric-mark/catalog-page"

export const Route = createFileRoute("/job-metric-marks")({
  component: JobMetricMarkBoard,
})
