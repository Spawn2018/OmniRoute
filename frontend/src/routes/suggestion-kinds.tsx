import { createFileRoute } from "@tanstack/react-router"
import { SuggestionKindBoard } from "@/features/suggestion-kind/catalog-page"

export const Route = createFileRoute("/suggestion-kinds")({
  component: SuggestionKindBoard,
})
