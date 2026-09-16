import { createFileRoute } from "@tanstack/react-router"
import { MarginFloorBoard } from "@/features/margin-floor/catalog-page"

export const Route = createFileRoute("/margin-floors")({
  component: MarginFloorBoard,
})
