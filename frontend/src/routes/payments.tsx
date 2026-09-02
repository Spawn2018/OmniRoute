import { createFileRoute } from "@tanstack/react-router"
import { BankPaymentPage } from "@/features/bank-payment/catalog-page"

export const Route = createFileRoute("/payments")({
  component: BankPaymentPage,
})
