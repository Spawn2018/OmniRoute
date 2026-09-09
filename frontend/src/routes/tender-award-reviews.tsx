import { createFileRoute } from "@tanstack/react-router"
import { AwardReviewDesk } from "@/features/tender-award-review/catalog-page"

export const Route = createFileRoute("/tender-award-reviews")({
  component: AwardReviewDesk,
})
