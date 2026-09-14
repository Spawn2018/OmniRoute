import { createFileRoute } from "@tanstack/react-router"
import { ProductTicketMarkDesk } from "@/features/product-ticket-mark/catalog-page"

export const Route = createFileRoute("/product-ticket-marks")({
  component: ProductTicketMarkDesk,
})
