import { createFileRoute } from "@tanstack/react-router"
import { MultiManningMarkBoard } from "@/features/multi-manning-mark/catalog-page"

export const Route = createFileRoute("/multi-manning-marks")({
  component: MultiManningMarkBoard,
})
