import { createFileRoute } from "@tanstack/react-router"
import { TimeToFixMarkDesk } from "@/features/time-to-fix-mark/catalog-page"

export const Route = createFileRoute("/time-to-fix-marks")({
  component: TimeToFixMarkDesk,
})
