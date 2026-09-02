import { createFileRoute } from "@tanstack/react-router"
import { ChinaRailPage } from "@/features/china-rail/catalog-page"

export const Route = createFileRoute("/china-rail")({
  component: ChinaRailPage,
})
