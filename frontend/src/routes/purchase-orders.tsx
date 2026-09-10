import { createFileRoute } from "@tanstack/react-router"
import { PurchaseOrderDesk } from "@/features/purchase-order/catalog-page"

export const Route = createFileRoute("/purchase-orders")({
  component: PurchaseOrderDesk,
})
