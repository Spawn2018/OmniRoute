import { createFileRoute } from "@tanstack/react-router"
import { FilingFkMarkDesk } from "@/features/filing-fk-mark/catalog-page"

export const Route = createFileRoute("/filing-fk-marks")({
  component: FilingFkMarkDesk,
})
