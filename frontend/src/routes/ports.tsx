import { createFileRoute } from "@tanstack/react-router"
import { PortCatalogPage } from "@/features/geography/ports-page"

export const Route = createFileRoute("/ports")({
  component: PortCatalogPage,
})
