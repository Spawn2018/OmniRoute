import { createFileRoute } from "@tanstack/react-router"
import { EdiMessagePage } from "@/features/edi-message/catalog-page"

export const Route = createFileRoute("/edi")({
  component: EdiMessagePage,
})
