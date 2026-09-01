import { createFileRoute } from "@tanstack/react-router"
import { LocationCatalogPage } from "@/features/geography/locations-page"

export const Route = createFileRoute("/locations")({
  component: LocationCatalogPage,
})
