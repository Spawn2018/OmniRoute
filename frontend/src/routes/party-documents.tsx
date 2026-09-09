import { createFileRoute } from "@tanstack/react-router"
import { PartyDocDesk } from "@/features/party-document/catalog-page"

export const Route = createFileRoute("/party-documents")({
  component: PartyDocDesk,
})
