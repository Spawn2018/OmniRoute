import { createFileRoute } from "@tanstack/react-router"
import { CollaborationMarkBoard } from "@/features/collaboration-mark/catalog-page"

export const Route = createFileRoute("/collaboration-marks")({
  component: CollaborationMarkBoard,
})
