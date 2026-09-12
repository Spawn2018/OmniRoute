import { createFileRoute } from "@tanstack/react-router"
import { DemoWipeMarkBoard } from "@/features/demo-wipe-mark/catalog-page"

export const Route = createFileRoute("/demo-wipe-marks")({
  component: DemoWipeMarkBoard,
})
