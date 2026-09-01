import { createFileRoute } from "@tanstack/react-router"
import { PartyScorecardCatalogPage } from "@/features/party-scorecards/catalog-page"

export const Route = createFileRoute("/party-scorecards")({
  component: PartyScorecardCatalogPage,
})
