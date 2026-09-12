import { createFileRoute } from "@tanstack/react-router"
import { VdaOdetteBoard } from "@/features/vda-odette-mark/catalog-page"

export const Route = createFileRoute("/vda-odette-marks")({
  component: VdaOdetteBoard,
})
