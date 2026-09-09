import { createFileRoute } from "@tanstack/react-router"
import { TwinDesk } from "@/features/twin-mark/catalog-page"

export const Route = createFileRoute("/twin-marks")({
  component: TwinDesk,
})
