import { createFileRoute } from "@tanstack/react-router"
import { QuoteInvoiceSettlementPage } from "@/features/quote-invoice-settlement/catalog-page"

export const Route = createFileRoute("/quote-invoices")({
  component: QuoteInvoiceSettlementPage,
})
