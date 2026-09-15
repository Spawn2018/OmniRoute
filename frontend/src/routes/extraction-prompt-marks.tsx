import { createFileRoute } from "@tanstack/react-router"
import { ExtractionPromptMarkDesk } from "@/features/extraction-prompt-mark/catalog-page"

export const Route = createFileRoute("/extraction-prompt-marks")({
  component: ExtractionPromptMarkDesk,
})
