import { createFileRoute } from "@tanstack/react-router"
import { IsoNis2Board } from "@/features/iso-nis2-mark/catalog-page"

export const Route = createFileRoute("/iso-nis2-marks")({
  component: IsoNis2Board,
})
