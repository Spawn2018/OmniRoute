import { createFileRoute } from "@tanstack/react-router"
import { LocalChargeMatchMarkDesk } from "@/features/local-charge-match-mark/catalog-page"

export const Route = createFileRoute("/local-charge-match-marks")({
  component: LocalChargeMatchMarkDesk,
})
