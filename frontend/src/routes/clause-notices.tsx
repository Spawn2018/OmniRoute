import { createFileRoute } from "@tanstack/react-router"
import { ClauseNoticeDesk } from "@/features/clause-notice/catalog-page"

export const Route = createFileRoute("/clause-notices")({
  component: ClauseNoticeDesk,
})
