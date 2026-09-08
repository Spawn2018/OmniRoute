import { createFileRoute } from "@tanstack/react-router"
import { BundleDesk } from "@/features/charge-template/catalog-page"

export const Route = createFileRoute("/charge-templates")({
  component: BundleDesk,
})
