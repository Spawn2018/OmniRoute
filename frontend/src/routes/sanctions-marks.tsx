import { createFileRoute } from "@tanstack/react-router"
import { SanctionsMarkDesk } from "@/features/sanctions-mark/catalog-page"

export const Route = createFileRoute("/sanctions-marks")({
  component: SanctionsMarkDesk,
})
