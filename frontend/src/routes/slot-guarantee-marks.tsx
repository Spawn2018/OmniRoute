import { createFileRoute } from "@tanstack/react-router"
import { SlotGuaranteeMarkBoard } from "@/features/slot-guarantee-mark/catalog-page"

export const Route = createFileRoute("/slot-guarantee-marks")({
  component: SlotGuaranteeMarkBoard,
})
