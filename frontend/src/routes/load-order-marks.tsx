import { createFileRoute } from "@tanstack/react-router"
import { LoadOrderMarkDesk } from "@/features/load-order-mark/catalog-page"

export const Route = createFileRoute("/load-order-marks")({
  component: LoadOrderMarkDesk,
})
