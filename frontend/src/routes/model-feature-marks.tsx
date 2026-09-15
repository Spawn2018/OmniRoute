import { createFileRoute } from "@tanstack/react-router"
import { ModelFeatureMarkDesk } from "@/features/model-feature-mark/catalog-page"

export const Route = createFileRoute("/model-feature-marks")({
  component: ModelFeatureMarkDesk,
})
