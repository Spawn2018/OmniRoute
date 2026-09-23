import { createFileRoute } from "@tanstack/react-router"
import { LocalChargeWarningMarkDesk } from "@/features/local-charge-warning-mark/catalog-page"

export const Route = createFileRoute("/local-charge-warning-marks")({
  component: LocalChargeWarningMarkDesk,
})
