import { createFileRoute } from "@tanstack/react-router"
import { CreditReviewCatalogPage } from "@/features/credit-reviews/catalog-page"

export const Route = createFileRoute("/credit-reviews")({
  component: CreditReviewCatalogPage,
})
