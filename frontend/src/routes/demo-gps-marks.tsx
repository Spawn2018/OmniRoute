import { createFileRoute } from "@tanstack/react-router"
import { DemoGpsMarkBoard } from "@/features/demo-gps-mark/catalog-page"

export const Route = createFileRoute("/demo-gps-marks")({
  component: DemoGpsMarkBoard,
})
