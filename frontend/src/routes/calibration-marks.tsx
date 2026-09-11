import { createFileRoute } from "@tanstack/react-router"
import { CalibrationMarkDesk } from "@/features/calibration-mark/catalog-page"

export const Route = createFileRoute("/calibration-marks")({
  component: CalibrationMarkDesk,
})
