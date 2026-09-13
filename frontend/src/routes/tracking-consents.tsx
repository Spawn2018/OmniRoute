import { createFileRoute } from "@tanstack/react-router"
import { TrackingConsentDesk } from "@/features/tracking-consent/catalog-page"

export const Route = createFileRoute("/tracking-consents")({
  component: TrackingConsentDesk,
})
