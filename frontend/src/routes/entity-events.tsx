import { createFileRoute } from "@tanstack/react-router"
import { EntityEventCatalogPage } from "@/features/entity-events/catalog-page"

export const Route = createFileRoute("/entity-events")({
  component: EntityEventCatalogPage,
})
