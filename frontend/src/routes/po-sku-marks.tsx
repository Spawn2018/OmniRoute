import { createFileRoute } from "@tanstack/react-router"
import { PoSkuMarkBoard } from "@/features/po-sku-mark/catalog-page"

export const Route = createFileRoute("/po-sku-marks")({
  component: PoSkuMarkBoard,
})
