import { createFileRoute } from "@tanstack/react-router"
import { BillingMarkDesk } from "@/features/billing-mark/catalog-page"

export const Route = createFileRoute("/billing-marks")({
  component: BillingMarkDesk,
})
