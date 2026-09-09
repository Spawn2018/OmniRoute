import { createFileRoute } from "@tanstack/react-router"
import { VerdictDesk } from "@/features/tender-win-loss/catalog-page"

export const Route = createFileRoute("/tender-win-losses")({
  component: VerdictDesk,
})
