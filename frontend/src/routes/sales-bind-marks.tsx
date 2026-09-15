import { createFileRoute } from "@tanstack/react-router"
import { SalesBindMarkDesk } from "@/features/sales-bind-mark/catalog-page"

export const Route = createFileRoute("/sales-bind-marks")({
  component: SalesBindMarkDesk,
})
