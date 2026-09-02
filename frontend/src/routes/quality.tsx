import { createFileRoute } from "@tanstack/react-router"
import { ExtractionQualityPage } from "@/features/extraction-quality/catalog-page"

export const Route = createFileRoute("/quality")({
  component: ExtractionQualityPage,
})
