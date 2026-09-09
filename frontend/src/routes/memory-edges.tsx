import { createFileRoute } from "@tanstack/react-router"
import { EdgeDesk } from "@/features/memory-edge/catalog-page"

export const Route = createFileRoute("/memory-edges")({
  component: EdgeDesk,
})
