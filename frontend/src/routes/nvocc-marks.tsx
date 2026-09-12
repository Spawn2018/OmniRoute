import { createFileRoute } from "@tanstack/react-router"
import { NvoccMarkBoard } from "@/features/nvocc-mark/catalog-page"

export const Route = createFileRoute("/nvocc-marks")({
  component: NvoccMarkBoard,
})
