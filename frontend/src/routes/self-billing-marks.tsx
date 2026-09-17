import { createFileRoute } from "@tanstack/react-router"
import { SelfBillingMarkDesk } from "@/features/self-billing-mark/catalog-page"

export const Route = createFileRoute("/self-billing-marks")({
  component: SelfBillingMarkDesk,
})
