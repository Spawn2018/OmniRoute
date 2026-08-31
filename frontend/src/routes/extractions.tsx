import { createFileRoute } from "@tanstack/react-router"
import { ExtractionQueuePage } from "@/features/extraction/queue-page"

export const Route = createFileRoute("/extractions")({
  component: ExtractionQueuePage,
})
