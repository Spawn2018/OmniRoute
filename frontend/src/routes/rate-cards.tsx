import { createFileRoute } from "@tanstack/react-router"
import { WhenDesk } from "@/features/rate-card/catalog-page"

export const Route = createFileRoute("/rate-cards")({
  component: WhenDesk,
})
