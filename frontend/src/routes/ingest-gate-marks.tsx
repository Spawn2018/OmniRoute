import { createFileRoute } from "@tanstack/react-router"
import { IngestGateMarkDesk } from "@/features/ingest-gate-mark/catalog-page"

export const Route = createFileRoute("/ingest-gate-marks")({
  component: IngestGateMarkDesk,
})
