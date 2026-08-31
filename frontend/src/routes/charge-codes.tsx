import { createFileRoute } from "@tanstack/react-router"
import { ChargeCodeCatalogPage } from "@/features/charge-codes/catalog-page"

export const Route = createFileRoute("/charge-codes")({
  component: ChargeCodeCatalogPage,
})
