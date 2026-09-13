import { createFileRoute } from "@tanstack/react-router"
import { QuoteCurrencyMarkBoard } from "@/features/quote-currency-mark/catalog-page"

export const Route = createFileRoute("/quote-currency-marks")({
  component: QuoteCurrencyMarkBoard,
})
