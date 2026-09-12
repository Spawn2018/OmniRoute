import { createFileRoute } from "@tanstack/react-router"
import { EDoreczeniaMarkBoard } from "@/features/e-doreczenia-mark/catalog-page"

export const Route = createFileRoute("/e-doreczenia-marks")({
  component: EDoreczeniaMarkBoard,
})
