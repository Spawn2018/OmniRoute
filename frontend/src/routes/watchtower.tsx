import { createFileRoute } from "@tanstack/react-router"
import { WatchtowerPage } from "@/features/watchtower/catalog-page"

export const Route = createFileRoute("/watchtower")({
  component: WatchtowerPage,
})
