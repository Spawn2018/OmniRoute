import { createFileRoute } from "@tanstack/react-router"
import { ECmrDesk } from "@/features/e-cmr-mark/catalog-page"

export const Route = createFileRoute("/e-cmr-marks")({
  component: ECmrDesk,
})
