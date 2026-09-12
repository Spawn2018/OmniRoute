import { createFileRoute } from "@tanstack/react-router"
import { DemoSimMarkBoard } from "@/features/demo-sim-mark/catalog-page"

export const Route = createFileRoute("/demo-sim-marks")({
  component: DemoSimMarkBoard,
})
