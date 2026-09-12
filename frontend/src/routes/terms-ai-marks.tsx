import { createFileRoute } from "@tanstack/react-router"
import { TermsAiMarkBoard } from "@/features/terms-ai-mark/catalog-page"

export const Route = createFileRoute("/terms-ai-marks")({
  component: TermsAiMarkBoard,
})
