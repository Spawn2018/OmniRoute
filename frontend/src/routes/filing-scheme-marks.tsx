import { createFileRoute } from "@tanstack/react-router"
import { FilingSchemeMarkDesk } from "@/features/filing-scheme-mark/catalog-page"

export const Route = createFileRoute("/filing-scheme-marks")({
  component: FilingSchemeMarkDesk,
})
