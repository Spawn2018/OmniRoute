import { createFileRoute } from "@tanstack/react-router"
import { BriefDesk } from "@/features/executive-mark/catalog-page"

export const Route = createFileRoute("/executive-marks")({
  component: BriefDesk,
})
