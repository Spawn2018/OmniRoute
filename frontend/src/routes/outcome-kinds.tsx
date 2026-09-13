import { createFileRoute } from "@tanstack/react-router"
import { OutcomeKindBoard } from "@/features/outcome-kind/catalog-page"

export const Route = createFileRoute("/outcome-kinds")({
  component: OutcomeKindBoard,
})
