import { createFileRoute } from "@tanstack/react-router"
import { SkontoDesk } from "@/features/cash-discount/catalog-page"

export const Route = createFileRoute("/cash-discounts")({
  component: SkontoDesk,
})
