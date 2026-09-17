import { createFileRoute } from "@tanstack/react-router"
import { PurchaseInvoiceDesk } from "@/features/purchase-invoice/catalog-page"

export const Route = createFileRoute("/purchase-invoices")({
  component: PurchaseInvoiceDesk,
})
