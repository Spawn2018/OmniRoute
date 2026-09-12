import { createFileRoute } from "@tanstack/react-router"
import { DiversionMarkBoard } from "@/features/diversion-mark/catalog-page"

export const Route = createFileRoute("/diversion-marks")({
  component: DiversionMarkBoard,
})
