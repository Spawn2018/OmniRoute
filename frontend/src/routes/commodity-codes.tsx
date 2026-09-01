import { createFileRoute } from "@tanstack/react-router"
import { CommodityCodeCatalogPage } from "@/features/commodity-codes/catalog-page"

export const Route = createFileRoute("/commodity-codes")({
  component: CommodityCodeCatalogPage,
})
