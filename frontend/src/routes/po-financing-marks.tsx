import { createFileRoute } from "@tanstack/react-router"
import { PoFinancingMarkDesk } from "@/features/po-financing-mark/catalog-page"

export const Route = createFileRoute("/po-financing-marks")({
  component: PoFinancingMarkDesk,
})
