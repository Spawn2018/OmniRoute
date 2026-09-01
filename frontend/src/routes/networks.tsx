import { createFileRoute } from "@tanstack/react-router"
import { NetworkCatalogPage } from "@/features/networks/catalog-page"

export const Route = createFileRoute("/networks")({
  component: NetworkCatalogPage,
})
