import { createFileRoute } from "@tanstack/react-router"
import { PoBatchMarkBoard } from "@/features/po-batch-mark/catalog-page"

export const Route = createFileRoute("/po-batch-marks")({
  component: PoBatchMarkBoard,
})
