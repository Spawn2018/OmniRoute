import { createFileRoute } from "@tanstack/react-router"
import { HandoverNoteDesk } from "@/features/handover-note/catalog-page"

export const Route = createFileRoute("/handover-notes")({
  component: HandoverNoteDesk,
})
