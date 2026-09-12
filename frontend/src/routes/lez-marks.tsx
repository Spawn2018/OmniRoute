import { createFileRoute } from "@tanstack/react-router"
import { LezMarkBoard } from "@/features/lez-mark/catalog-page"

export const Route = createFileRoute("/lez-marks")({
  component: LezMarkBoard,
})
