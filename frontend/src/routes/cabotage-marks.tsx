import { createFileRoute } from "@tanstack/react-router"
import { CabotageMarkPage } from "@/features/cabotage-mark/catalog-page"

export const Route = createFileRoute("/cabotage-marks")({
  component: CabotageMarkPage,
})
