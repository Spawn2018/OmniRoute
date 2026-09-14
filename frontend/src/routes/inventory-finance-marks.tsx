import { createFileRoute } from "@tanstack/react-router"
import { InventoryFinanceMarkDesk } from "@/features/inventory-finance-mark/catalog-page"

export const Route = createFileRoute("/inventory-finance-marks")({
  component: InventoryFinanceMarkDesk,
})
