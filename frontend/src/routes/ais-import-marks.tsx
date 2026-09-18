import { createFileRoute } from "@tanstack/react-router"
import { AisImportMarkDesk } from "@/features/ais-import-mark/catalog-page"

export const Route = createFileRoute("/ais-import-marks")({
  component: AisImportMarkDesk,
})
