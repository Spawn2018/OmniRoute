import { createFileRoute } from "@tanstack/react-router"
import { CustomerPoMarkBoard } from "@/features/customer-po-mark/catalog-page"

export const Route = createFileRoute("/customer-po-marks")({
  component: CustomerPoMarkBoard,
})
