import { createFileRoute } from "@tanstack/react-router"
import { AllocationLevelBoard } from "@/features/allocation-level/catalog-page"

export const Route = createFileRoute("/allocation-levels")({
  component: AllocationLevelBoard,
})
