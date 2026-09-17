import { createFileRoute } from "@tanstack/react-router"
import { InvoiceAllocMarkDesk } from "@/features/invoice-alloc-mark/catalog-page"

export const Route = createFileRoute("/invoice-alloc-marks")({
  component: InvoiceAllocMarkDesk,
})
