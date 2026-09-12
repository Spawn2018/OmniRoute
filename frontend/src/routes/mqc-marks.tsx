import { createFileRoute } from "@tanstack/react-router"
import { MqcBoard } from "@/features/mqc-mark/catalog-page"

export const Route = createFileRoute("/mqc-marks")({
  component: MqcBoard,
})
