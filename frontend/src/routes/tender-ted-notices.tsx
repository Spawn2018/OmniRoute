import { createFileRoute } from "@tanstack/react-router"
import { TedDesk } from "@/features/tender-ted-notice/catalog-page"

export const Route = createFileRoute("/tender-ted-notices")({
  component: TedDesk,
})
