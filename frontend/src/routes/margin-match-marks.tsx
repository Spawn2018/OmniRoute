import { createFileRoute } from "@tanstack/react-router"
import { MarginMatchMarkDesk } from "@/features/margin-match-mark/catalog-page"

export const Route = createFileRoute("/margin-match-marks")({
  component: MarginMatchMarkDesk,
})
