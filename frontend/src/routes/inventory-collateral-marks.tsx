import { createFileRoute } from "@tanstack/react-router"
import { InventoryCollateralMarkDesk } from "@/features/inventory-collateral-mark/catalog-page"

export const Route = createFileRoute("/inventory-collateral-marks")({
  component: InventoryCollateralMarkDesk,
})
