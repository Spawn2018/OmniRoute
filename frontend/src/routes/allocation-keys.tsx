import { createFileRoute } from "@tanstack/react-router"
import { AllocationKeyBoard } from "@/features/allocation-key/catalog-page"

export const Route = createFileRoute("/allocation-keys")({
  component: AllocationKeyBoard,
})
