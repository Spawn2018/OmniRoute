import { createFileRoute } from "@tanstack/react-router"
import { MakeOrBuyMarkDesk } from "@/features/make-or-buy-mark/catalog-page"

export const Route = createFileRoute("/make-or-buy-marks")({
  component: MakeOrBuyMarkDesk,
})
