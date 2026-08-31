import { createFileRoute } from "@tanstack/react-router"
import { RateLineCatalogPage } from "@/features/rate-lines/catalog-page"

export const Route = createFileRoute("/rate-lines")({
  component: RateLineCatalogPage,
})
