import { createFileRoute } from "@tanstack/react-router"
import { FairShareBoard } from "@/features/fair-share-mark/catalog-page"

export const Route = createFileRoute("/fair-share-marks")({
  component: FairShareBoard,
})
