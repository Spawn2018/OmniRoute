import { createFileRoute } from "@tanstack/react-router"
import { CustomerSopCatalogPage } from "@/features/customer-sops/catalog-page"

export const Route = createFileRoute("/customer-sops")({
  component: CustomerSopCatalogPage,
})
