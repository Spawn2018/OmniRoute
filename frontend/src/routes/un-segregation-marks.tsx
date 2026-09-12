import { createFileRoute } from "@tanstack/react-router"
import { UnSegregationMarkBoard } from "@/features/un-segregation-mark/catalog-page"

export const Route = createFileRoute("/un-segregation-marks")({
  component: UnSegregationMarkBoard,
})
