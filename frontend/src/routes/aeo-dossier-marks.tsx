import { createFileRoute } from "@tanstack/react-router"
import { AeoDossierMarkDesk } from "@/features/aeo-dossier-mark/catalog-page"

export const Route = createFileRoute("/aeo-dossier-marks")({
  component: AeoDossierMarkDesk,
})
