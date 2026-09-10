import { createFileRoute } from "@tanstack/react-router"
import { SnapshotDesk } from "@/features/plan-snapshot/catalog-page"

export const Route = createFileRoute("/plan-snapshots")({
  component: SnapshotDesk,
})
