import { createFileRoute } from "@tanstack/react-router"
import { DemandSnapshotMarkBoard } from "@/features/demand-snapshot-mark/catalog-page"

export const Route = createFileRoute("/demand-snapshot-marks")({
  component: DemandSnapshotMarkBoard,
})
