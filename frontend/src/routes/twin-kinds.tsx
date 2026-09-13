import { createFileRoute } from "@tanstack/react-router"
import { TwinKindBoard } from "@/features/twin-kind/catalog-page"

export const Route = createFileRoute("/twin-kinds")({
  component: TwinKindBoard,
})
