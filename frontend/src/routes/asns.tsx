import { createFileRoute } from "@tanstack/react-router"
import { AsnDesk } from "@/features/asn/catalog-page"

export const Route = createFileRoute("/asns")({
  component: AsnDesk,
})
