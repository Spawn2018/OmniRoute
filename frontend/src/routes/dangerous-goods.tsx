import { createFileRoute } from "@tanstack/react-router"
import { DangerousGoodCatalogPage } from "@/features/dangerous-goods/catalog-page"

export const Route = createFileRoute("/dangerous-goods")({
  component: DangerousGoodCatalogPage,
})
