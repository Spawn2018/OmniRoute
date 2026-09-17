import { createFileRoute } from "@tanstack/react-router"
import { InvoiceMatchMarkDesk } from "@/features/invoice-match-mark/catalog-page"

export const Route = createFileRoute("/invoice-match-marks")({
  component: InvoiceMatchMarkDesk,
})
