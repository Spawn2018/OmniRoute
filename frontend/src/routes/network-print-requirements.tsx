import { createFileRoute } from "@tanstack/react-router"
import { NetworkPrintRequirementDesk } from "@/features/network-print-requirement/catalog-page"

export const Route = createFileRoute("/network-print-requirements")({
  component: NetworkPrintRequirementDesk,
})
