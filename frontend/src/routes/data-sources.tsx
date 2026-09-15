import { createFileRoute } from "@tanstack/react-router"
import { DataSourceDesk } from "@/features/data-source/catalog-page"

export const Route = createFileRoute("/data-sources")({
  component: DataSourceDesk,
})
