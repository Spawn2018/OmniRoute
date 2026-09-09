import { createFileRoute } from "@tanstack/react-router"
import { SchemeDesk } from "@/features/monitoring-scheme/catalog-page"

export const Route = createFileRoute("/monitoring-schemes")({
  component: SchemeDesk,
})
