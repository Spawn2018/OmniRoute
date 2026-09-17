import { createFileRoute } from "@tanstack/react-router"
import { ProductTicketDesk } from "@/features/product-ticket/catalog-page"

export const Route = createFileRoute("/product-tickets")({
  component: ProductTicketDesk,
})
