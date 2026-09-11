import { createFileRoute } from "@tanstack/react-router"
import { CombinedTransportDesk } from "@/features/combined-transport-mark/catalog-page"

export const Route = createFileRoute("/combined-transport-marks")({
  component: CombinedTransportDesk,
})
