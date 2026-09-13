import { createFileRoute } from "@tanstack/react-router"
import { AutonomyLevelBoard } from "@/features/autonomy-level/catalog-page"

export const Route = createFileRoute("/autonomy-levels")({
  component: AutonomyLevelBoard,
})
