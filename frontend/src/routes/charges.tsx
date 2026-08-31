import { createFileRoute } from "@tanstack/react-router"
import { ChargeCatalogPage } from "@/features/charges/catalog-page"

export const Route = createFileRoute("/charges")({
  component: ChargeCatalogPage,
})
