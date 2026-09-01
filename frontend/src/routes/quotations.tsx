import { createFileRoute } from "@tanstack/react-router"
import { QuotationCatalogPage } from "@/features/quotations/catalog-page"

export const Route = createFileRoute("/quotations")({
  component: QuotationCatalogPage,
})
