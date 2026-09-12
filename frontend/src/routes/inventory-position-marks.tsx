import { createFileRoute } from "@tanstack/react-router"
import { InventoryPositionBoard } from "@/features/inventory-position-mark/catalog-page"

export const Route = createFileRoute("/inventory-position-marks")({
  component: InventoryPositionBoard,
})
