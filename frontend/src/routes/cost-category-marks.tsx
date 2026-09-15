import { createFileRoute } from "@tanstack/react-router"
import { CostCategoryMarkDesk } from "@/features/cost-category-mark/catalog-page"

export const Route = createFileRoute("/cost-category-marks")({
  component: CostCategoryMarkDesk,
})
