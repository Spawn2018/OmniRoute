import { createFileRoute } from "@tanstack/react-router"
import { CodBoard } from "@/features/cod-instruction/catalog-page"

export const Route = createFileRoute("/cod")({
  component: CodBoard,
})
