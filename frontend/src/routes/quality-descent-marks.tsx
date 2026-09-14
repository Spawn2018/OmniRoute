import { createFileRoute } from "@tanstack/react-router"
import { QualityDescentMarkDesk } from "@/features/quality-descent-mark/catalog-page"

export const Route = createFileRoute("/quality-descent-marks")({
  component: QualityDescentMarkDesk,
})
