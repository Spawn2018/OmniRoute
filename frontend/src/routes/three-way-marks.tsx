import { createFileRoute } from "@tanstack/react-router"
import { ThreeWayMarkBoard } from "@/features/three-way-mark/catalog-page"

export const Route = createFileRoute("/three-way-marks")({
  component: ThreeWayMarkBoard,
})
