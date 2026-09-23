import { createFileRoute } from "@tanstack/react-router"
import { LocalChargeBindMarkDesk } from "@/features/local-charge-bind-mark/catalog-page"

export const Route = createFileRoute("/local-charge-bind-marks")({
  component: LocalChargeBindMarkDesk,
})
