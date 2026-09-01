import { createFileRoute } from "@tanstack/react-router"
import { PartyCatalogPage } from "@/features/parties/catalog-page"

export const Route = createFileRoute("/parties")({
  component: PartyCatalogPage,
})
