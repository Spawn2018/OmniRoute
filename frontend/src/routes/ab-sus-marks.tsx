import { createFileRoute } from "@tanstack/react-router"
import { AbSusMarkBoard } from "@/features/ab-sus-mark/catalog-page"

export const Route = createFileRoute("/ab-sus-marks")({
  component: AbSusMarkBoard,
})
