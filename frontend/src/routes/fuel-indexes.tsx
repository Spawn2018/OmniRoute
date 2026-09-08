import { createFileRoute } from "@tanstack/react-router"
import { IndexDesk } from "@/features/fuel-index/catalog-page"

export const Route = createFileRoute("/fuel-indexes")({
  component: IndexDesk,
})
