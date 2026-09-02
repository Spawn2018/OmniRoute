import { createFileRoute } from "@tanstack/react-router"
import { AiCopilotPage } from "@/features/ai-copilot/catalog-page"

export const Route = createFileRoute("/ai")({
  component: AiCopilotPage,
})
