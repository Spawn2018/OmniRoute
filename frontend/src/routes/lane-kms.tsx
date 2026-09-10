import { createFileRoute } from "@tanstack/react-router"
import { LaneKmDesk } from "@/features/lane-km/catalog-page"

export const Route = createFileRoute("/lane-kms")({
  component: LaneKmDesk,
})
