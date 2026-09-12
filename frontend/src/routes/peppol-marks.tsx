import { createFileRoute } from "@tanstack/react-router"
import { PeppolDesk } from "@/features/peppol-mark/catalog-page"

export const Route = createFileRoute("/peppol-marks")({
  component: PeppolDesk,
})
