import { createFileRoute } from "@tanstack/react-router"
import { NbpRateCatalogPage } from "@/features/nbp-rates/catalog-page"

export const Route = createFileRoute("/nbp-rates")({
  component: NbpRateCatalogPage,
})
