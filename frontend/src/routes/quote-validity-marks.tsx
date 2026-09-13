import { createFileRoute } from "@tanstack/react-router"
import { QuoteValidityMarkBoard } from "@/features/quote-validity-mark/catalog-page"

export const Route = createFileRoute("/quote-validity-marks")({
  component: QuoteValidityMarkBoard,
})
