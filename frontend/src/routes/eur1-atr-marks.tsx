import { createFileRoute } from "@tanstack/react-router"
import { Eur1AtrBoard } from "@/features/eur1-atr-mark/catalog-page"

export const Route = createFileRoute("/eur1-atr-marks")({
  component: Eur1AtrBoard,
})
