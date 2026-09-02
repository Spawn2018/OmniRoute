import { createFileRoute } from "@tanstack/react-router"
import { SalesInvoicePage } from "@/features/sales-invoice/catalog-page"

export const Route = createFileRoute("/invoices")({
  component: SalesInvoicePage,
})
