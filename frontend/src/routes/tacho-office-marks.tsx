import { createFileRoute } from "@tanstack/react-router"
import { TachoOfficeMarkBoard } from "@/features/tacho-office-mark/catalog-page"

export const Route = createFileRoute("/tacho-office-marks")({
  component: TachoOfficeMarkBoard,
})
