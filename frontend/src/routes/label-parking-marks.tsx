import { createFileRoute } from "@tanstack/react-router"
import { LabelParkingMarkBoard } from "@/features/label-parking-mark/catalog-page"

export const Route = createFileRoute("/label-parking-marks")({
  component: LabelParkingMarkBoard,
})
