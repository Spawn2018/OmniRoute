import { createFileRoute } from "@tanstack/react-router"
import { FieldConfidenceMarkDesk } from "@/features/field-confidence-mark/catalog-page"

export const Route = createFileRoute("/field-confidence-marks")({
  component: FieldConfidenceMarkDesk,
})
