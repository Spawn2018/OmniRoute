import { createFileRoute } from "@tanstack/react-router"
import { StopGroupBoard } from "@/features/stop-group/catalog-page"

export const Route = createFileRoute("/stop-groups")({
  component: StopGroupBoard,
})
