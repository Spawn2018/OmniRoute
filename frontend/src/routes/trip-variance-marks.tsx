import { createFileRoute } from "@tanstack/react-router"
import { TripVarianceMarkDesk } from "@/features/trip-variance-mark/catalog-page"

export const Route = createFileRoute("/trip-variance-marks")({
  component: TripVarianceMarkDesk,
})
