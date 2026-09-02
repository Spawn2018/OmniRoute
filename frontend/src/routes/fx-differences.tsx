import { createFileRoute } from "@tanstack/react-router"
import { FxDifferencePage } from "@/features/fx-difference/catalog-page"

export const Route = createFileRoute("/fx-differences")({
  component: FxDifferencePage,
})
