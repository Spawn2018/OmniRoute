import { createFileRoute } from "@tanstack/react-router"
import { CampaignMarkDesk } from "@/features/campaign-mark/catalog-page"

export const Route = createFileRoute("/campaign-marks")({
  component: CampaignMarkDesk,
})
