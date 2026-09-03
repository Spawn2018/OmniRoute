import { createFileRoute } from "@tanstack/react-router"
import { OutboxCatalogPage } from "@/features/outbox/catalog-page"

export const Route = createFileRoute("/outbox")({
  component: OutboxCatalogPage,
})
