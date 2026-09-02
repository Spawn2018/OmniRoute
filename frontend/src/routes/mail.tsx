import { createFileRoute } from "@tanstack/react-router"
import { MailIntegrationPage } from "@/features/mail-integration/catalog-page"

export const Route = createFileRoute("/mail")({
  component: MailIntegrationPage,
})
