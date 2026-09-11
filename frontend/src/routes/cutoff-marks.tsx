import { createFileRoute } from "@tanstack/react-router"
import { CutoffMarkDesk } from "@/features/cutoff-mark/catalog-page"

export const Route = createFileRoute("/cutoff-marks")({
  component: CutoffMarkDesk,
})
