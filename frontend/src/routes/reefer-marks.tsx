import { createFileRoute } from "@tanstack/react-router"
import { ReeferMarkBoard } from "@/features/reefer-mark/catalog-page"

export const Route = createFileRoute("/reefer-marks")({
  component: ReeferMarkBoard,
})
