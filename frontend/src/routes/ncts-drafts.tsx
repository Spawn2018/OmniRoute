import { createFileRoute } from "@tanstack/react-router"
import { NctsDraftDesk } from "@/features/ncts-draft/catalog-page"

export const Route = createFileRoute("/ncts-drafts")({
  component: NctsDraftDesk,
})
