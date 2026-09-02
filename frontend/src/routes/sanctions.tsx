import { createFileRoute } from "@tanstack/react-router"
import { SanctionsPage } from "@/features/sanctions/catalog-page"

export const Route = createFileRoute("/sanctions")({
  component: SanctionsPage,
})
