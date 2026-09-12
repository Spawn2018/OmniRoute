import { createFileRoute } from "@tanstack/react-router"
import { EccnBoard } from "@/features/eccn-mark/catalog-page"

export const Route = createFileRoute("/eccn-marks")({
  component: EccnBoard,
})
