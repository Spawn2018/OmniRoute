import { createFileRoute } from "@tanstack/react-router"
import { GdprPage } from "@/features/gdpr/catalog-page"

export const Route = createFileRoute("/gdpr")({
  component: GdprPage,
})
