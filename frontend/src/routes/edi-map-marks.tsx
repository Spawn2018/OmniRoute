import { createFileRoute } from "@tanstack/react-router"
import { EdiMapMarkDesk } from "@/features/edi-map-mark/catalog-page"

export const Route = createFileRoute("/edi-map-marks")({
  component: EdiMapMarkDesk,
})
