import { createFileRoute } from "@tanstack/react-router"
import { CfoNarrativeMarkDesk } from "@/features/cfo-narrative-mark/catalog-page"

export const Route = createFileRoute("/cfo-narrative-marks")({
  component: CfoNarrativeMarkDesk,
})
