import { createFileRoute } from "@tanstack/react-router"
import { PortSurchargeCatalogPage } from "@/features/port-surcharges/catalog-page"

export const Route = createFileRoute("/port-surcharges")({
  component: PortSurchargeCatalogPage,
})
