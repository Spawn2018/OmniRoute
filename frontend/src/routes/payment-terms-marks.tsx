import { createFileRoute } from "@tanstack/react-router"
import { PaymentTermsMarkBoard } from "@/features/payment-terms-mark/catalog-page"

export const Route = createFileRoute("/payment-terms-marks")({
  component: PaymentTermsMarkBoard,
})
